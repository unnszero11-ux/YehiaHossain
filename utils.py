"""Utility functions for Worker Service."""
import os
import random
import string
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from pathlib import Path

# Setup logging
def setup_logging(log_level: str = 'INFO', log_to_file: bool = True) -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger('card_checker')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(logs_dir / 'worker.log')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

def load_file_lines(filepath: str) -> List[str]:
    """Load lines from a file, ignoring comments and empty lines."""
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Filter out comments and empty lines
    return [
        line.strip() 
        for line in lines 
        if line.strip() and not line.strip().startswith('#')
    ]

def load_cards(filepath: str = 'cards.txt') -> List[Dict[str, str]]:
    """Load cards from file.
    
    Format: card_number|exp_month|exp_year
    Example: 4242424242424242|12|2025
    """
    lines = load_file_lines(filepath)
    cards = []
    
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 3:
            cards.append({
                'card_number': parts[0].strip(),
                'exp_month': parts[1].strip(),
                'exp_year': parts[2].strip()
            })
    
    return cards

def load_zip_codes(filepath: str = 'zip.txt') -> List[str]:
    """Load ZIP codes from file."""
    return load_file_lines(filepath)

def load_proxies(filepath: str = 'proxies.txt') -> List[str]:
    """Load proxies from file."""
    return load_file_lines(filepath)

def parse_proxy(proxy_string: str) -> Optional[Dict[str, str]]:
    """Parse proxy string into components.
    
    Supported formats:
    1. ip:port
    2. ip:port:username:password
    3. username:password@ip:port
    4. http://ip:port
    5. http://username:password@ip:port
    6. socks5://username:password@ip:port
    """
    try:
        # Remove protocol if present
        protocol = 'http'
        if '://' in proxy_string:
            protocol, proxy_string = proxy_string.split('://', 1)
        
        # Check for username:password@ip:port format
        if '@' in proxy_string:
            auth, server = proxy_string.split('@', 1)
            username, password = auth.split(':', 1)
            ip, port = server.split(':', 1)
            return {
                'server': f'{protocol}://{ip}:{port}',
                'username': username,
                'password': password
            }
        
        # Check for ip:port:username:password format
        parts = proxy_string.split(':')
        if len(parts) == 4:
            return {
                'server': f'{protocol}://{parts[0]}:{parts[1]}',
                'username': parts[2],
                'password': parts[3]
            }
        
        # Simple ip:port format
        if len(parts) == 2:
            return {
                'server': f'{protocol}://{parts[0]}:{parts[1]}'
            }
        
        return None
    except Exception:
        return None

def get_random_proxy(proxies: List[str]) -> Optional[Dict[str, str]]:
    """Get a random proxy from the list."""
    if not proxies:
        return None
    
    proxy_string = random.choice(proxies)
    return parse_proxy(proxy_string)

def generate_random_name() -> str:
    """Generate a random name."""
    try:
        import names
        return names.get_full_name()
    except ImportError:
        # Fallback if names library not available
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia']
        return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_phone() -> str:
    """Generate a random US phone number."""
    area_code = random.randint(200, 999)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"{area_code}{exchange}{number}"

def generate_random_email(name: str = None) -> str:
    """Generate a random email address."""
    if not name:
        name = generate_random_name()
    
    username = name.lower().replace(' ', '.')
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    random_num = random.randint(100, 999)
    
    return f"{username}{random_num}@{random.choice(domains)}"

def mask_card_number(card_number: str) -> str:
    """Mask card number, showing only last 4 digits."""
    if len(card_number) < 4:
        return card_number
    return f"{'*' * (len(card_number) - 4)}{card_number[-4:]}"

def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp for logging."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def save_result_to_file(result: Dict[str, Any], filepath: str = 'logs/results.log'):
    """Save check result to file."""
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    with open(filepath, 'a', encoding='utf-8') as f:
        timestamp = format_timestamp()
        card = mask_card_number(result.get('card', ''))
        status = result.get('result', 'unknown')
        website = result.get('website', 'unknown')
        message = result.get('message', '')
        
        f.write(f"[{timestamp}] {website.upper()} | {card} | {status.upper()} | {message}\n")

def generate_api_key(length: int = 32) -> str:
    """Generate a random API key."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
