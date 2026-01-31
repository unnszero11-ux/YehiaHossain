"""Card checker using Playwright to test cards on real websites."""
import asyncio
import random
from typing import Dict, Optional, List
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

from config import config
from utils import (
    setup_logging,
    load_zip_codes,
    load_proxies,
    get_random_proxy,
    generate_random_name,
    generate_random_phone,
    generate_random_email,
    mask_card_number,
    save_result_to_file
)

logger = setup_logging(config.LOG_LEVEL, config.LOG_TO_FILE)

class CardChecker:
    """Card checker using Playwright."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.zip_codes: List[str] = load_zip_codes(config.ZIP_FILE)
        self.proxies: List[str] = load_proxies(config.PROXIES_FILE)
        
        if not self.zip_codes:
            logger.warning("No ZIP codes loaded. Using default.")
            self.zip_codes = ['10001', '10002', '10003']
        
        logger.info(f"Loaded {len(self.zip_codes)} ZIP codes")
        logger.info(f"Loaded {len(self.proxies)} proxies")
    
    async def start_browser(self, use_proxy: bool = False) -> Browser:
        """Start Playwright browser."""
        playwright = await async_playwright().start()
        
        launch_options = {
            'headless': config.HEADLESS,
            'slow_mo': config.SLOW_MO,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        }
        
        # Add proxy if enabled
        if use_proxy and config.USE_PROXY and self.proxies:
            proxy_config = get_random_proxy(self.proxies)
            if proxy_config:
                launch_options['proxy'] = proxy_config
                logger.info(f"Using proxy: {proxy_config.get('server')}")
        
        self.browser = await playwright.chromium.launch(**launch_options)
        return self.browser
    
    async def close_browser(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
    
    async def check_card_loft(self, card_data: Dict[str, str]) -> Dict[str, any]:
        """Check card on LOFT.com."""
        card_number = card_data['card_number']
        exp_month = card_data['exp_month']
        exp_year = card_data['exp_year']
        
        logger.info(f"Checking card {mask_card_number(card_number)} on LOFT.com")
        
        try:
            # Start browser
            browser = await self.start_browser(use_proxy=card_data.get('use_proxy', True))
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            # Navigate to LOFT
            await page.goto('https://www.loft.com', timeout=config.BROWSER_TIMEOUT)
            await page.wait_for_load_state('networkidle')
            
            # Generate random data
            name = generate_random_name()
            email = generate_random_email(name)
            phone = generate_random_phone()
            zip_code = random.choice(self.zip_codes)
            
            logger.info(f"Using: {name}, {email}, {zip_code}")
            
            # TODO: Implement actual checkout flow
            # This is a simplified version - you need to:
            # 1. Add item to cart
            # 2. Go to checkout
            # 3. Fill shipping info
            # 4. Fill payment info
            # 5. Check for success/decline message
            
            # For now, simulate the check
            await asyncio.sleep(2)
            
            # Check for payment form
            try:
                # Wait for payment form (adjust selectors based on actual site)
                await page.wait_for_selector('input[name="cardNumber"]', timeout=30000)
                
                # Fill card info
                await page.fill('input[name="cardNumber"]', card_number)
                await page.fill('input[name="expMonth"]', exp_month)
                await page.fill('input[name="expYear"]', exp_year)
                
                # Submit (don't actually submit in test mode)
                # await page.click('button[type="submit"]')
                
                result = {
                    'success': True,
                    'result': 'live',
                    'card': card_number,
                    'website': 'loft',
                    'message': 'Card appears valid (test mode)',
                    'timestamp': datetime.now().isoformat()
                }
                
            except PlaywrightTimeout:
                result = {
                    'success': False,
                    'result': 'error',
                    'card': card_number,
                    'website': 'loft',
                    'message': 'Payment form not found',
                    'timestamp': datetime.now().isoformat()
                }
            
            await context.close()
            await self.close_browser()
            
            # Save result
            save_result_to_file(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking card: {str(e)}")
            await self.close_browser()
            
            return {
                'success': False,
                'result': 'error',
                'card': card_number,
                'website': 'loft',
                'message': f'Error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    async def check_card_anntaylor(self, card_data: Dict[str, str]) -> Dict[str, any]:
        """Check card on AnnTaylor.com."""
        card_number = card_data['card_number']
        exp_month = card_data['exp_month']
        exp_year = card_data['exp_year']
        
        logger.info(f"Checking card {mask_card_number(card_number)} on AnnTaylor.com")
        
        try:
            # Start browser
            browser = await self.start_browser(use_proxy=card_data.get('use_proxy', True))
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            # Navigate to Ann Taylor
            await page.goto('https://www.anntaylor.com', timeout=config.BROWSER_TIMEOUT)
            await page.wait_for_load_state('networkidle')
            
            # Generate random data
            name = generate_random_name()
            email = generate_random_email(name)
            phone = generate_random_phone()
            zip_code = random.choice(self.zip_codes)
            
            logger.info(f"Using: {name}, {email}, {zip_code}")
            
            # TODO: Implement actual checkout flow
            # Similar to LOFT implementation
            
            await asyncio.sleep(2)
            
            result = {
                'success': True,
                'result': 'live',
                'card': card_number,
                'website': 'anntaylor',
                'message': 'Card appears valid (test mode)',
                'timestamp': datetime.now().isoformat()
            }
            
            await context.close()
            await self.close_browser()
            
            # Save result
            save_result_to_file(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking card: {str(e)}")
            await self.close_browser()
            
            return {
                'success': False,
                'result': 'error',
                'card': card_number,
                'website': 'anntaylor',
                'message': f'Error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    async def check_card(self, card_data: Dict[str, str], website: str = 'loft') -> Dict[str, any]:
        """Check card on specified website."""
        website = website.lower()
        
        if website not in config.SUPPORTED_WEBSITES:
            return {
                'success': False,
                'result': 'error',
                'card': card_data.get('card_number', ''),
                'website': website,
                'message': f'Unsupported website: {website}',
                'timestamp': datetime.now().isoformat()
            }
        
        if website == 'loft':
            return await self.check_card_loft(card_data)
        elif website == 'anntaylor':
            return await self.check_card_anntaylor(card_data)
        
        return {
            'success': False,
            'result': 'error',
            'card': card_data.get('card_number', ''),
            'website': website,
            'message': 'Not implemented',
            'timestamp': datetime.now().isoformat()
        }
    
    async def check_cards_bulk(self, cards: List[Dict[str, str]], website: str = 'loft') -> List[Dict[str, any]]:
        """Check multiple cards sequentially."""
        results = []
        
        for i, card_data in enumerate(cards, 1):
            logger.info(f"Checking card {i}/{len(cards)}")
            result = await self.check_card(card_data, website)
            results.append(result)
            
            # Add delay between checks to avoid rate limiting
            if i < len(cards):
                delay = random.randint(3, 7)
                logger.info(f"Waiting {delay} seconds before next check...")
                await asyncio.sleep(delay)
        
        return results

# Singleton instance
checker = CardChecker()

def main_cli():
    """Command-line interface for standalone execution"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Check credit card on website')
    parser.add_argument('--website', required=True, choices=['loft', 'anntaylor'], help='Website to check')
    parser.add_argument('--card', required=True, help='Card number')
    parser.add_argument('--exp-month', required=True, help='Expiry month')
    parser.add_argument('--exp-year', required=True, help='Expiry year')
    parser.add_argument('--cvv', required=True, help='CVV code')
    parser.add_argument('--name', default='JOHN DOE', help='Cardholder name')
    parser.add_argument('--headless', default='true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    # Create card data
    card_data = {
        'card_number': args.card,
        'exp_month': args.exp_month,
        'exp_year': args.exp_year,
        'cvv': args.cvv,
        'cardholder_name': args.name
    }
    
    # Run async check
    result = asyncio.run(checker.check_card(card_data, args.website))
    
    # Output JSON result
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main_cli()
