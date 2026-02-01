import os
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
            'requests', 'bs4', 'scapy', 'colorama', 
            'argparse', 'pyfiglet', 'progress'
        ]
        self.platform = platform.system().lower()
        self.python_version = sys.version_info
        
    def check_python_version(self):
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 7):
            print(f"[ERROR] Python 3.7+ required. You have {self.python_version.major}.{self.python_version.minor}")
            return False
        return True
    
    def check_modules(self):
        missing_modules = []
        for module in self.required_modules:
            try:
                if module == 'bs4':
                    importlib.import_module('bs4')
                elif module == 'pyfiglet':
                    importlib.import_module('pyfiglet')
                elif module == 'progress':
                    importlib.import_module('progress')
                else:
                    importlib.import_module(module)
            except ImportError:
                missing_modules.append(module)
        return missing_modules
    
    def install_modules(self, modules):
        print(f"[SYSTEM] Installing {len(modules)} missing modules...")
        for module in modules:
            try:
                if module == 'bs4':
                    module_name = 'beautifulsoup4'
                elif module == 'progress':
                    module_name = 'progress'
                else:
                    module_name = module
                
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name, '--quiet'])
                print(f"[SUCCESS] Installed: {module_name}")
                time.sleep(0.5)
            except Exception as e:
                print(f"[FAILED] Could not install {module}: {e}")
                return False
        return True
    
    def setup_directories(self):
        directories = ['src', 'plugin', 'logs', 'data', 'results']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"[CREATED] Directory: {directory}")
        
        plugin_files = ['DDOS.py', 'DOS.py', 'SQL_injection.py', 
                       'XSS.py', 'deface.py', 'recon.py', 'vuln_scanner.py']
        
        for pfile in plugin_files:
            plugin_path = os.path.join('plugin', pfile)
            if not os.path.exists(plugin_path):
                with open(plugin_path, 'w') as f:
                    f.write(f"# {pfile.replace('.py', '').replace('_', ' ').title()} Plugin\n")
                    f.write("# Auto-generated placeholder\n")
                    f.write("print('Plugin not yet implemented')\n")
    
    def get_system_info(self):
        info = {
            'platform': self.platform,
            'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': platform.node(),
            'working_directory': os.getcwd(),
            'timestamp': datetime.now().isoformat()
        }
        self.system_info = info
        return info
    
    def initialize(self):
        print("[AIO TOOLS] System Initialization")
        print("=" * 50)
        
        if not self.check_python_version():
            sys.exit(1)
        
        self.get_system_info()
        print(f"[PLATFORM] {self.system_info['platform'].upper()} detected")
        print(f"[PYTHON] Version {self.system_info['python_version']}")
        
        missing = self.check_modules()
        if missing:
            print(f"[MISSING] {len(missing)} modules not found")
            install = input("[PROMPT] Install missing modules automatically? (y/n): ").strip().lower()
            if install == 'y':
                if not self.install_modules(missing):
                    print("[ERROR] Installation failed. Exiting.")
                    sys.exit(1)
            else:
                print("[INFO] Manual installation required.")
                print(f"[LIST] Missing: {', '.join(missing)}")
                sys.exit(1)
        
        self.setup_directories()
        print("[SUCCESS] System initialization complete")
        print("=" * 50)
        return True

if __name__ == "__main__":
    sys_setup = SystemSetup()
    sys_setup.initialize()