"""Flask API server for Card Checker Worker Service."""
import asyncio
from functools import wraps
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config
from card_checker import checker
from utils import setup_logging, mask_card_number

logger = setup_logging(config.LOG_LEVEL, config.LOG_TO_FILE)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"] if config.ENABLE_RATE_LIMIT else []
)

# Statistics
stats = {
    'total_checks': 0,
    'live_cards': 0,
    'declined_cards': 0,
    'errors': 0,
    'start_time': None
}

def require_api_key(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required', 'message': 'Missing X-API-Key header'}), 401
        
        if api_key != config.API_KEY:
            return jsonify({'error': 'Invalid API key'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def check_ip_whitelist():
    """Check if request IP is whitelisted."""
    if not config.ALLOWED_IPS or config.ALLOWED_IPS == ['']:
        return True
    
    client_ip = request.remote_addr
    return client_ip in config.ALLOWED_IPS

@app.before_request
def before_request():
    """Check IP whitelist before processing request."""
    if not check_ip_whitelist():
        return jsonify({
            'error': 'Access denied',
            'message': 'Your IP is not whitelisted'
        }), 403

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Card Checker Worker',
        'version': '1.0.0',
        'supported_websites': config.SUPPORTED_WEBSITES
    }), 200

@app.route('/api/check-card', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
def check_card():
    """Check a single card.
    
    Request body:
    {
        "website": "loft",
        "card_number": "4242424242424242",
        "exp_month": "12",
        "exp_year": "2025",
        "use_proxy": true
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['website', 'card_number', 'exp_month', 'exp_year']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing required field',
                    'field': field
                }), 400
        
        # Validate website
        website = data['website'].lower()
        if website not in config.SUPPORTED_WEBSITES:
            return jsonify({
                'error': 'Unsupported website',
                'supported': config.SUPPORTED_WEBSITES
            }), 400
        
        # Prepare card data
        card_data = {
            'card_number': data['card_number'],
            'exp_month': data['exp_month'],
            'exp_year': data['exp_year'],
            'use_proxy': data.get('use_proxy', True)
        }
        
        logger.info(f"Checking card {mask_card_number(card_data['card_number'])} on {website}")
        
        # Run async check
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(checker.check_card(card_data, website))
        loop.close()
        
        # Update stats
        stats['total_checks'] += 1
        if result['result'] == 'live':
            stats['live_cards'] += 1
        elif result['result'] == 'declined':
            stats['declined_cards'] += 1
        else:
            stats['errors'] += 1
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in check_card: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/check-cards-bulk', methods=['POST'])
@require_api_key
@limiter.limit("2 per minute")
def check_cards_bulk():
    """Check multiple cards.
    
    Request body:
    {
        "website": "loft",
        "cards": [
            {"card_number": "4242...", "exp_month": "12", "exp_year": "2025"},
            {"card_number": "5555...", "exp_month": "06", "exp_year": "2026"}
        ],
        "use_proxy": true
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'website' not in data or 'cards' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['website', 'cards']
            }), 400
        
        # Validate website
        website = data['website'].lower()
        if website not in config.SUPPORTED_WEBSITES:
            return jsonify({
                'error': 'Unsupported website',
                'supported': config.SUPPORTED_WEBSITES
            }), 400
        
        # Validate cards
        cards = data['cards']
        if not isinstance(cards, list) or len(cards) == 0:
            return jsonify({
                'error': 'Invalid cards data',
                'message': 'cards must be a non-empty array'
            }), 400
        
        # Limit bulk size
        if len(cards) > 50:
            return jsonify({
                'error': 'Too many cards',
                'message': 'Maximum 50 cards per bulk request',
                'received': len(cards)
            }), 400
        
        # Add use_proxy to each card
        use_proxy = data.get('use_proxy', True)
        for card in cards:
            card['use_proxy'] = use_proxy
        
        logger.info(f"Bulk checking {len(cards)} cards on {website}")
        
        # Run async bulk check
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(checker.check_cards_bulk(cards, website))
        loop.close()
        
        # Update stats
        for result in results:
            stats['total_checks'] += 1
            if result['result'] == 'live':
                stats['live_cards'] += 1
            elif result['result'] == 'declined':
                stats['declined_cards'] += 1
            else:
                stats['errors'] += 1
        
        # Summary
        summary = {
            'total': len(results),
            'live': sum(1 for r in results if r['result'] == 'live'),
            'declined': sum(1 for r in results if r['result'] == 'declined'),
            'errors': sum(1 for r in results if r['result'] == 'error')
        }
        
        return jsonify({
            'success': True,
            'summary': summary,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in check_cards_bulk: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/metrics', methods=['GET'])
@require_api_key
def get_metrics():
    """Get service metrics."""
    import time
    from datetime import datetime
    
    if stats['start_time'] is None:
        stats['start_time'] = time.time()
    
    uptime = time.time() - stats['start_time']
    
    success_rate = 0
    if stats['total_checks'] > 0:
        success_rate = (stats['live_cards'] / stats['total_checks']) * 100
    
    return jsonify({
        'total_checks': stats['total_checks'],
        'live_cards': stats['live_cards'],
        'declined_cards': stats['declined_cards'],
        'errors': stats['errors'],
        'success_rate': round(success_rate, 2),
        'uptime_seconds': int(uptime),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/config', methods=['GET'])
@require_api_key
def get_config():
    """Get service configuration (non-sensitive)."""
    return jsonify({
        'headless': config.HEADLESS,
        'use_proxy': config.USE_PROXY,
        'proxy_rotation': config.PROXY_ROTATION,
        'supported_websites': config.SUPPORTED_WEBSITES,
        'rate_limit_enabled': config.ENABLE_RATE_LIMIT
    }), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors."""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please slow down.'
    }), 429

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong'
    }), 500

if __name__ == '__main__':
    # Validate configuration
    if not config.validate():
        logger.error("Configuration validation failed!")
        logger.error("Please update your .env file with a secure API_KEY")
        exit(1)
    
    # Initialize start time
    import time
    stats['start_time'] = time.time()
    
    logger.info("="*60)
    logger.info("Card Checker Worker Service")
    logger.info("="*60)
    logger.info(f"Host: {config.WORKER_HOST}")
    logger.info(f"Port: {config.WORKER_PORT}")
    logger.info(f"Headless: {config.HEADLESS}")
    logger.info(f"Use Proxy: {config.USE_PROXY}")
    logger.info(f"Rate Limit: {config.ENABLE_RATE_LIMIT}")
    logger.info(f"Supported Websites: {', '.join(config.SUPPORTED_WEBSITES)}")
    logger.info("="*60)
    logger.info("Starting server...")
    
    # Run Flask app
    app.run(
        host=config.WORKER_HOST,
        port=config.WORKER_PORT,
        debug=False
    )
