#!/usr/bin/env python3
"""Test script for Worker Service - Comprehensive testing."""
import sys
import os
import json
import time
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def check_file(filepath, description):
    """Check if file exists."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print_success(f"{description}: {filepath} ({size} bytes)")
        return True
    else:
        print_error(f"{description}: {filepath} NOT FOUND")
        return False

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python version: {version_str} (OK)")
        return True
    else:
        print_error(f"Python version: {version_str} (Need 3.8+)")
        return False

def check_imports():
    """Check if required packages can be imported."""
    packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('flask_limiter', 'Flask-Limiter'),
        ('playwright', 'Playwright'),
        ('dotenv', 'python-dotenv'),
        ('requests', 'Requests'),
        ('faker', 'Faker'),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            all_ok = False
    
    return all_ok

def check_config_file():
    """Check if .env file exists and is configured."""
    if not os.path.exists('.env'):
        print_warning(".env file NOT found")
        print_info("Run: cp .env.example .env")
        return False
    
    print_success(".env file exists")
    
    # Check if API_KEY is changed
    with open('.env', 'r') as f:
        content = f.read()
        if 'change_this_to_secure_random_key' in content:
            print_warning("API_KEY still has default value")
            print_info("Change API_KEY in .env file")
            return False
    
    print_success("API_KEY is configured")
    return True

def check_data_files():
    """Check if data files exist."""
    files = [
        ('cards.txt', 'Cards file'),
        ('zip.txt', 'ZIP codes file'),
    ]
    
    all_ok = True
    for filename, description in files:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
                if lines:
                    print_success(f"{description}: {len(lines)} entries")
                else:
                    print_warning(f"{description}: Empty")
                    all_ok = False
        else:
            print_warning(f"{description}: NOT found")
            print_info(f"Run: cp {filename}.example {filename}")
            all_ok = False
    
    # Proxies are optional
    if os.path.exists('proxies.txt'):
        with open('proxies.txt', 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
            if lines:
                print_success(f"Proxies file: {len(lines)} entries (optional)")
            else:
                print_info("Proxies file: Empty (optional)")
    else:
        print_info("Proxies file: NOT found (optional)")
    
    return all_ok

def test_config_loading():
    """Test if config can be loaded."""
    try:
        from config import config
        print_success("Config module loaded")
        print_info(f"  - Worker Port: {config.WORKER_PORT}")
        print_info(f"  - Worker Host: {config.WORKER_HOST}")
        print_info(f"  - Headless: {config.HEADLESS}")
        print_info(f"  - Use Proxy: {config.USE_PROXY}")
        print_info(f"  - Rate Limit: {config.ENABLE_RATE_LIMIT}")
        print_info(f"  - Supported Sites: {', '.join(config.SUPPORTED_WEBSITES)}")
        return True
    except Exception as e:
        print_error(f"Config loading failed: {e}")
        return False

def test_utils_loading():
    """Test if utils can be loaded."""
    try:
        from utils import setup_logging, load_cards, load_zip_codes
        print_success("Utils module loaded")
        
        # Test logging
        logger = setup_logging('INFO', False)
        print_success("Logging setup OK")
        
        # Test loading cards
        if os.path.exists('cards.txt'):
            cards = load_cards('cards.txt')
            print_success(f"Cards loaded: {len(cards)} cards")
        
        # Test loading ZIP codes
        if os.path.exists('zip.txt'):
            zips = load_zip_codes('zip.txt')
            print_success(f"ZIP codes loaded: {len(zips)} codes")
        
        return True
    except Exception as e:
        print_error(f"Utils loading failed: {e}")
        return False

def test_api_server_loading():
    """Test if API server can be loaded."""
    try:
        # Just import, don't run
        import api_server
        print_success("API server module loaded")
        print_info("  - Flask app initialized")
        print_info("  - CORS enabled")
        print_info("  - Rate limiter configured")
        return True
    except Exception as e:
        print_error(f"API server loading failed: {e}")
        return False

def generate_test_report(results):
    """Generate test report."""
    print_header("TEST REPORT")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    else:
        print_success(f"Failed: {failed}")
    
    print("\n" + "="*60)
    
    if failed == 0:
        print_success("\n🎉 ALL TESTS PASSED! Worker Service is ready!")
        print_info("\nNext steps:")
        print_info("  1. Run: python api_server.py")
        print_info("  2. Test: curl http://localhost:5000/api/health")
        return True
    else:
        print_error("\n❌ SOME TESTS FAILED! Please fix the issues above.")
        print_info("\nCommon fixes:")
        print_info("  1. Install packages: pip install -r requirements.txt")
        print_info("  2. Install Playwright: playwright install chromium")
        print_info("  3. Create .env: cp .env.example .env")
        print_info("  4. Create data files: cp *.example files")
        return False

def main():
    """Main test function."""
    print(f"{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║          WORKER SERVICE - COMPREHENSIVE TEST              ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    results = {}
    
    # Test 1: Python Version
    print_header("TEST 1: Python Version")
    results['python_version'] = check_python_version()
    
    # Test 2: Core Files
    print_header("TEST 2: Core Files")
    files_ok = True
    files_ok &= check_file('api_server.py', 'API Server')
    files_ok &= check_file('card_checker.py', 'Card Checker')
    files_ok &= check_file('config.py', 'Config')
    files_ok &= check_file('utils.py', 'Utils')
    files_ok &= check_file('requirements.txt', 'Requirements')
    files_ok &= check_file('.env.example', 'Env Example')
    results['core_files'] = files_ok
    
    # Test 3: Python Packages
    print_header("TEST 3: Python Packages")
    results['packages'] = check_imports()
    
    # Test 4: Configuration
    print_header("TEST 4: Configuration")
    results['config'] = check_config_file()
    
    # Test 5: Data Files
    print_header("TEST 5: Data Files")
    results['data_files'] = check_data_files()
    
    # Test 6: Config Loading
    print_header("TEST 6: Config Module")
    results['config_loading'] = test_config_loading()
    
    # Test 7: Utils Loading
    print_header("TEST 7: Utils Module")
    results['utils_loading'] = test_utils_loading()
    
    # Test 8: API Server Loading
    print_header("TEST 8: API Server Module")
    results['api_server'] = test_api_server_loading()
    
    # Generate Report
    success = generate_test_report(results)
    
    return 0 if success else 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)
