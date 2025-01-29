import os
import sys
import platform
import pkg_resources
from colorama import init, Fore, Style
import requests

# Initialize colorama for cross-platform colored output
init()

def print_step(message: str, status: str = 'info') -> None:
    """
    Print formatted status message with emoji and color.
    
    Args:
        message (str): Message to print
        status (str): Status type (info, success, error, warning)
    """
    colors = {
        'info': Fore.BLUE,
        'success': Fore.GREEN,
        'error': Fore.RED,
        'warning': Fore.YELLOW
    }
    
    icons = {
        'info': 'ℹ️',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️'
    }
    
    color = colors.get(status, Fore.WHITE)
    icon = icons.get(status, 'ℹ️')
    print(f"{color}{icon} {message}{Style.RESET_ALL}")

def check_python_version() -> bool:
    """
    Check if Python version meets requirements.
    
    Returns:
        bool: True if version is OK, False otherwise
    """
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version >= required_version:
        print_step(f"Python version {current_version.major}.{current_version.minor} OK", 'success')
        return True
    else:
        print_step(f"Python version {current_version.major}.{current_version.minor} is too old. Need 3.8+", 'error')
        return False

def check_required_packages() -> bool:
    """
    Check if all required packages are installed.
    
    Returns:
        bool: True if all packages are installed, False otherwise
    """
    required_packages = {
        'requests': 'requests',
        'pandas': 'pandas',
        'colorama': 'colorama',
        'schedule': 'schedule',
        'python-dotenv': 'dotenv'
    }
    
    all_installed = True
    for package_name, import_name in required_packages.items():
        try:
            pkg_resources.get_distribution(package_name)
            print_step(f"Package {package_name} is installed", 'success')
        except pkg_resources.DistributionNotFound:
            print_step(f"Package {package_name} is missing", 'error')
            all_installed = False
    
    return all_installed

def check_internet_connection() -> bool:
    """
    Check if there's internet connectivity to Airtable API.
    
    Returns:
        bool: True if connection is OK, False otherwise
    """
    try:
        requests.get("https://api.airtable.com", timeout=5)
        print_step("Internet connection OK", 'success')
        return True
    except requests.RequestException:
        print_step("No internet connection or Airtable API unreachable", 'error')
        return False

def check_environment() -> bool:
    """
    Check all required environment variables.
    
    Returns:
        bool: True if all environment variables are set, False otherwise
    """
    missing_vars = []
    
    # Check API Key
    if not os.getenv('AIRTABLE_API_KEY'):
        missing_vars.append('AIRTABLE_API_KEY')
    
    # Check Base ID
    if not os.getenv('AIRTABLE_BASE_ID'):
        missing_vars.append('AIRTABLE_BASE_ID')
    
    if missing_vars:
        print_step(f"Missing environment variables: {', '.join(missing_vars)}", 'error')
        print("\nPlease set the variables:")
        print("Windows:")
        for var in missing_vars:
            print(f"set {var}=your_{var.lower()}_here")
        print("\nLinux/Mac:")
        for var in missing_vars:
            print(f"export {var}=your_{var.lower()}_here")
        return False
    
    print_step("All environment variables are set", 'success')
    return True

def check_write_permissions() -> bool:
    """
    Check if the script has write permissions in the current directory.
    
    Returns:
        bool: True if write permissions OK, False otherwise
    """
    try:
        test_file = "test_permissions.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print_step("Write permissions OK", 'success')
        return True
    except Exception as e:
        print_step(f"No write permissions in current directory: {str(e)}", 'error')
        return False

def main():
    """
    Run all environment checks.
    """
    print("\n=== Airtable Backup Tool Environment Check ===\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Internet Connection", check_internet_connection),
        ("Environment Variables", check_environment),
        ("Write Permissions", check_write_permissions)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n>> Checking {check_name}...")
        results.append(check_func())
    
    print("\n=== Summary ===")
    if all(results):
        print_step("All checks passed! You're ready to go!", 'success')
        return True
    else:
        print_step("Some checks failed. Please fix the issues above.", 'error')
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)