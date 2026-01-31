"""Configuration management for Worker Service."""
import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Worker Service Configuration."""
    
    # Server Settings
    WORKER_PORT: int = int(os.getenv('WORKER_PORT', '5000'))
    WORKER_HOST: str = os.getenv('WORKER_HOST', '0.0.0.0')
    API_KEY: str = os.getenv('API_KEY', 'change_this_to_secure_random_key')
    
    # Main App Integration
    MAIN_APP_URL: str = os.getenv('MAIN_APP_URL', 'https://v1cojc6udw.preview.c24.airoapp.ai')
    MAIN_APP_API_KEY: str = os.getenv('MAIN_APP_API_KEY', '')
    AUTO_SEND_RESULTS: bool = os.getenv('AUTO_SEND_RESULTS', 'true').lower() == 'true'
    
    # Browser Settings
    HEADLESS: bool = os.getenv('HEADLESS', 'false').lower() == 'true'
    BROWSER_TIMEOUT: int = int(os.getenv('BROWSER_TIMEOUT', '120000'))
    SLOW_MO: int = int(os.getenv('SLOW_MO', '100'))
    
    # Proxy Settings
    USE_PROXY: bool = os.getenv('USE_PROXY', 'true').lower() == 'true'
    PROXY_ROTATION: bool = os.getenv('PROXY_ROTATION', 'true').lower() == 'true'
    
    # Security
    ALLOWED_IPS: List[str] = os.getenv('ALLOWED_IPS', '127.0.0.1,::1').split(',')
    ENABLE_RATE_LIMIT: bool = os.getenv('ENABLE_RATE_LIMIT', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_TO_FILE: bool = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
    
    # File Paths
    CARDS_FILE: str = 'cards.txt'
    ZIP_FILE: str = 'zip.txt'
    PROXIES_FILE: str = 'proxies.txt'
    LOGS_DIR: str = 'logs'
    
    # Supported Websites
    SUPPORTED_WEBSITES = ['loft', 'anntaylor']
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if cls.API_KEY == 'change_this_to_secure_random_key':
            print("⚠️  WARNING: Using default API_KEY. Please change it in .env file!")
            return False
        return True
    
    @classmethod
    def get_website_url(cls, website: str) -> Optional[str]:
        """Get website URL."""
        urls = {
            'loft': 'https://www.loft.com',
            'anntaylor': 'https://www.anntaylor.com'
        }
        return urls.get(website.lower())

config = Config()
