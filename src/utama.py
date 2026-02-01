import os
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
        self.plugins_dir = "plugin"
        self.plugins = {}
        self.load_plugins()
        
    def display_banner(self):
        banner = pyfiglet.figlet_format("AIO TOOLS", font="slant")
        print(Fore.CYAN + banner)
        print(Fore.YELLOW + f"Version: {self.version} | Author: {self.author}")
        print(Fore.GREEN + "=" * 70)
        print(Fore.MAGENTA + "Advanced All-In-One Security Testing Framework")
        print(Fore.GREEN + "=" * 70)
    
    def load_plugins(self):
        if not os.path.exists(self.plugins_dir):
            print(f"[ERROR] Plugin directory '{self.plugins_dir}' not found")
            return
        
        plugin_files = [f for f in os.listdir(self.plugins_dir) if f.endswith('.py')]
        
        for pfile in plugin_files:
            plugin_name = pfile.replace('.py', '')
            plugin_path = os.path.join(self.plugins_dir, pfile)
            
            try:
                with open(plugin_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 10:
                        self.plugins[plugin_name] = {
                            'path': plugin_path,
                            'size': os.path.getsize(plugin_path),
                            'lines': len(lines)
                        }
            except:
                continue
    
    def show_menu(self):
        print(Fore.BLUE + "\n" + "=" * 70)
        print(Fore.YELLOW + "MAIN MENU")
        print(Fore.BLUE + "=" * 70)
        
        categories = {
            '1': {'name': 'DDOS Tools', 'plugins': ['DDOS']},
            '2': {'name': 'DOS Tools', 'plugins': ['DOS']},
            '3': {'name': 'SQL Injection', 'plugins': ['SQL_injection']},
            '4': {'name': 'XSS Tools', 'plugins': ['XSS']},
            '5': {'name': 'Web Defacement', 'plugins': ['deface']},
            '6': {'name': 'Reconnaissance', 'plugins': ['recon']},
            '7': {'name': 'Vulnerability Scanner', 'plugins': ['vuln_scanner']},
            '8': {'name': 'System Information', 'plugins': []},
            '9': {'name': 'Exit', 'plugins': []}
        }
        
        for key, value in categories.items():
            if key == '8':
                print(Fore.CYAN + f"[{key}] {value['name']}")
            elif key == '9':
                print(Fore.RED + f"[{key}] {value['name']}")
            else:
                print(Fore.GREEN + f"[{key}] {value['name']}")
        
        print(Fore.BLUE + "=" * 70)
    
    def run_plugin(self, plugin_name):
        plugin_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")
        
        if not os.path.exists(plugin_path):
            print(Fore.RED + f"[ERROR] Plugin '{plugin_name}' not found!")
            return False
        
        try:
            print(Fore.YELLOW + f"\n[LOADING] Executing {plugin_name}...")
            time.sleep(1)
            
            with open(plugin_path, 'r') as f:
                exec(f.read())
            
            return True
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to execute plugin: {e}")
            return False
    
    def system_info(self):
        print(Fore.CYAN + "\n" + "=" * 70)
        print(Fore.YELLOW + "SYSTEM INFORMATION")
        print(Fore.CYAN + "=" * 70)
        
        import platform
        import psutil
        
        info = {
            'System': platform.system(),
            'Node Name': platform.node(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'Python Version': platform.python_version(),
            'CPU Cores': psutil.cpu_count(),
            'Total RAM': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'Available RAM': f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            'Disk Usage': f"{psutil.disk_usage('/').percent}%",
            'Current Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for key, value in info.items():
            print(Fore.GREEN + f"{key:<20}: {Fore.WHITE}{value}")
        
        print(Fore.CYAN + "\n" + "=" * 70)
        print(Fore.YELLOW + "LOADED PLUGINS")
        print(Fore.CYAN + "=" * 70)
        
        if self.plugins:
            for plugin, data in self.plugins.items():
                status = Fore.GREEN + "✓ READY" if data['lines'] > 300 else Fore.YELLOW + "⚠ PARTIAL"
                print(Fore.CYAN + f"{plugin:<20} {status:<15} {data['lines']:>4} lines")
        else:
            print(Fore.RED + "No plugins loaded")
    
    def start(self):
        self.display_banner()
        
        parser = argparse.ArgumentParser(description='AIO Tools - Security Framework')
        parser.add_argument('--plugin', type=str, help='Run specific plugin directly')
        parser.add_argument('--info', action='store_true', help='Show system information')
        
        args = parser.parse_args()
        
        if args.plugin:
            self.run_plugin(args.plugin)
            return
        
        if args.info:
            self.system_info()
            return
        
        while True:
            self.show_menu()
            
            try:
                choice = input(Fore.MAGENTA + "\n[SELECT] Enter your choice (1-9): ").strip()
                
                if choice == '1':
                    self.run_plugin('DDOS')
                elif choice == '2':
                    self.run_plugin('DOS')
                elif choice == '3':
                    self.run_plugin('SQL_injection')
                elif choice == '4':
                    self.run_plugin('XSS')
                elif choice == '5':
                    self.run_plugin('deface')
                elif choice == '6':
                    self.run_plugin('recon')
                elif choice == '7':
                    self.run_plugin('vuln_scanner')
                elif choice == '8':
                    self.system_info()
                elif choice == '9':
                    print(Fore.RED + "\n[EXIT] Shutting down AIO Tools...")
                    time.sleep(1)
                    print(Fore.GREEN + "[GOODBYE] Stay secure!\n")
                    break
                else:
                    print(Fore.RED + "[ERROR] Invalid choice!")
                
                input(Fore.YELLOW + "\n[PRESS ENTER] to continue...")
                
            except KeyboardInterrupt:
                print(Fore.RED + "\n\n[INTERRUPT] Shutting down...")
                break
            except Exception as e:
                print(Fore.RED + f"[ERROR] {e}")

if __name__ == "__main__":
    try:
        main = AIOToolsMain()
        main.start()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[INTERRUPT] Terminated by user")
    except Exception as e:
        print(Fore.RED + f"[FATAL ERROR] {e}")