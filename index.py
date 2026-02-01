import os
import sys
import subprocess
import platform
from colorama import init, Fore, Style

init(autoreset=True)

def check_requirements():
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.YELLOW + "AIO TOOLS - REQUIREMENT CHECK")
    print(Fore.CYAN + "="*70)
    
    required_packages = [
        'requests',
        'beautifulsoup4',
        'colorama',
        'pyfiglet'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(Fore.GREEN + f"[✓] {package}")
        except ImportError:
            print(Fore.RED + f"[✗] {package}")
            missing.append(package)
    
    return missing

def install_packages(packages):
    print(Fore.YELLOW + f"\nInstalling {len(packages)} missing packages...")
    
    for package in packages:
        try:
            if package == 'beautifulsoup4':
                package_name = 'beautifulsoup4'
            else:
                package_name = package
            
            print(Fore.CYAN + f"Installing {package_name}...")
            
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name, '-q'])
            print(Fore.GREEN + f"[SUCCESS] {package_name} installed")
        
        except Exception as e:
            print(Fore.RED + f"[FAILED] {package}: {e}")
            return False
    
    return True

def setup_environment():
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.YELLOW + "AIO TOOLS - ENVIRONMENT SETUP")
    print(Fore.CYAN + "="*70)
    
    directories = ['src', 'plugin', 'logs', 'data', 'results', 'reports']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(Fore.GREEN + f"[CREATED] {directory}/")
        else:
            print(Fore.CYAN + f"[EXISTS] {directory}/")
    
    required_files = {
        'src/system.py': '''import os
import sys
import platform
import subprocess
import importlib
import json
import time
from datetime import datetime

class SystemSetup:
    def __init__(self):
        self.system_info = {}
        self.required_modules = [
            'requests', 'bs4', 'colorama', 
            'argparse', 'pyfiglet'
        ]
        self.platform = platform.system().lower()
        self.python_version = sys.version_info
''',
        'src/utama.py': '''import os
import sys
import time
import argparse
from colorama import init, Fore, Style
import pyfiglet
import json
from datetime import datetime

init(autoreset=True)

class AIOToolsMain:
    def __init__(self):
        self.version = "1.0.0"
        self.author = "AIO Security Team"
''',
        'src/support.py': '''import json
import time
import hashlib
import base64
import uuid
import random
import string
from datetime import datetime, timedelta

class SupportUtils:
    @staticmethod
    def generate_session_id():
        return str(uuid.uuid4())
'''
    }
    
    for file_path, content in required_files.items():
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(Fore.GREEN + f"[CREATED] {file_path}")
    
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.GREEN + "[SETUP COMPLETE] AIO Tools environment ready!")
    print(Fore.CYAN + "="*70)

def display_welcome():
    try:
        import pyfiglet
        banner = pyfiglet.figlet_format("AIO TOOLS", font="slant")
        print(Fore.CYAN + banner)
    except:
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.YELLOW + "AIO TOOLS - Advanced Security Framework")
        print(Fore.CYAN + "="*70)
    
    print(Fore.MAGENTA + "Version: 1.0.0 | Multi-Platform | All-In-One")
    print(Fore.GREEN + "="*70)
    print(Fore.YELLOW + "Features:")
    print(Fore.CYAN + "• DDOS/DOS Tools")
    print(Fore.CYAN + "• SQL Injection Scanner")
    print(Fore.CYAN + "• XSS Detection")
    print(Fore.CYAN + "• Web Vulnerability Scanner")
    print(Fore.CYAN + "• Reconnaissance Tools")
    print(Fore.CYAN + "• Location Tracking")
    print(Fore.CYAN + "• Auto-Exploitation")
    print(Fore.GREEN + "="*70)

def check_platform():
    system = platform.system().lower()
    
    print(Fore.CYAN + f"\n[PLATFORM] {system.upper()} detected")
    
    if system == 'windows':
        print(Fore.YELLOW + "[INFO] Running on Windows")
        return 'windows'
    elif system == 'linux':
        distro = platform.freedesktop_os_release().get('NAME', 'Linux')
        print(Fore.YELLOW + f"[INFO] Running on {distro}")
        return 'linux'
    elif system == 'darwin':
        print(Fore.YELLOW + "[INFO] Running on macOS")
        return 'macos'
    else:
        print(Fore.YELLOW + f"[INFO] Running on {system}")
        return system

def setup_permissions():
    system = platform.system().lower()
    
    if system == 'linux' or system == 'darwin':
        print(Fore.YELLOW + "\n[PERMISSIONS] Checking file permissions...")
        
        scripts = ['main.py', 'index.py']
        for script in scripts:
            if os.path.exists(script):
                try:
                    os.chmod(script, 0o755)
                    print(Fore.GREEN + f"[SET] {script} is executable")
                except:
                    print(Fore.RED + f"[ERROR] Could not set permissions for {script}")

def run_main():
    print(Fore.YELLOW + "\n[STARTING] AIO Tools...")
    
    if os.path.exists('main.py'):
        print(Fore.GREEN + "[LAUNCH] Starting main application...\n")
        print(Fore.CYAN + "="*70)
        
        try:
            subprocess.run([sys.executable, 'main.py'])
        except KeyboardInterrupt:
            print(Fore.RED + "\n[INTERRUPT] Application stopped")
        except Exception as e:
            print(Fore.RED + f"[ERROR] {e}")
    else:
        print(Fore.RED + "[ERROR] main.py not found!")
        print(Fore.YELLOW + "[ACTION] Creating main.py...")
        
        main_content = '''#!/usr/bin/env python3
"""
AIO Tools - Main Entry Point
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.utama import AIOToolsMain
    
    if __name__ == "__main__":
        app = AIOToolsMain()
        app.start()
        
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please run setup first: python index.py")
    sys.exit(1)
'''
        
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        print(Fore.GREEN + "[CREATED] main.py")
        print(Fore.YELLOW + "[RESTART] Please run again")
        sys.exit(0)

def main():
    display_welcome()
    
    missing_packages = check_requirements()
    
    if missing_packages:
        print(Fore.YELLOW + f"\n[ACTION] {len(missing_packages)} packages missing")
        install = input(Fore.CYAN + "Install automatically? (y/n): ").strip().lower()
        
        if install == 'y':
            if not install_packages(missing_packages):
                print(Fore.RED + "\n[ERROR] Installation failed. Exiting.")
                sys.exit(1)
        else:
            print(Fore.RED + "\n[ERROR] Required packages missing. Exiting.")
            print(Fore.YELLOW + f"Missing: {', '.join(missing_packages)}")
            sys.exit(1)
    
    setup_environment()
    check_platform()
    setup_permissions()
    
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.YELLOW + "[READY] AIO Tools is ready to run!")
    print(Fore.CYAN + "="*70)
    
    run_now = input(Fore.MAGENTA + "\nStart AIO Tools now? (y/n): ").strip().lower()
    
    if run_now == 'y':
        run_main()
    else:
        print(Fore.YELLOW + "\n[INFO] You can start AIO Tools later with:")
        print(Fore.GREEN + "  python main.py")
        print(Fore.CYAN + "  or")
        print(Fore.GREEN + "  ./main.py (Linux/Mac)")
        print(Fore.YELLOW + "\n[EXITING] Setup complete!")
    
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.GREEN + "Thank you for using AIO Tools!")
    print(Fore.CYAN + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[INTERRUPT] Setup cancelled")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n[FATAL ERROR] {e}")
        sys.exit(1)