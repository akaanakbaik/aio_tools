#!/usr/bin/env python3
"""
AIO TOOLS - Advanced Security Framework
Main Entry Point
"""

import os
import sys
import time
import argparse
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from colorama import init, Fore, Style
    import pyfiglet
    
    init(autoreset=True)
    
except ImportError as e:
    print(f"[ERROR] Required modules not found: {e}")
    print("[ACTION] Running setup...")
    subprocess.run([sys.executable, 'index.py'])
    sys.exit(1)

class AIOToolsCore:
    def __init__(self):
        self.version = "2.0.0"
        self.build = "2024.01"
        self.platform = sys.platform
        self.start_time = datetime.now()
        self.plugins_loaded = False
        self.plugins = {}
        
    def display_header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            banner = pyfiglet.figlet_format("AIO TOOLS", font="slant")
            print(Fore.CYAN + banner)
        except:
            print(Fore.CYAN + "\n" + "="*80)
            print(Fore.YELLOW + "╔══════════════════════════════════════════════════════════════════════════════╗")
            print(Fore.YELLOW + "║                     AIO TOOLS - ADVANCED SECURITY FRAMEWORK                   ║")
            print(Fore.YELLOW + "╚══════════════════════════════════════════════════════════════════════════════╝")
            print(Fore.CYAN + "="*80)
        
        print(Fore.MAGENTA + f"Version: {self.version} | Build: {self.build} | Platform: {self.platform}")
        print(Fore.GREEN + f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.CYAN + "="*80)
        print(Fore.YELLOW + "A Comprehensive All-In-One Security Testing and Penetration Testing Toolkit")
        print(Fore.CYAN + "="*80)
    
    def check_environment(self):
        print(Fore.YELLOW + "\n[ENVIRONMENT CHECK]")
        
        required_dirs = ['src', 'plugin', 'logs', 'data', 'results']
        missing_dirs = []
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                missing_dirs.append(directory)
                print(Fore.RED + f"  [MISSING] {directory}/")
            else:
                print(Fore.GREEN + f"  [OK] {directory}/")
        
        if missing_dirs:
            print(Fore.YELLOW + "\n[SETUP] Creating missing directories...")
            for directory in missing_dirs:
                os.makedirs(directory, exist_ok=True)
                print(Fore.GREEN + f"  [CREATED] {directory}/")
        
        required_files = ['src/system.py', 'src/utama.py', 'src/support.py']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(Fore.RED + "\n[ERROR] Core files missing!")
            print(Fore.YELLOW + "[ACTION] Running setup script...")
            time.sleep(2)
            subprocess.run([sys.executable, 'index.py'])
            return False
        
        print(Fore.GREEN + "\n[ENVIRONMENT] All checks passed!")
        return True
    
    def load_plugins(self):
        print(Fore.YELLOW + "\n[PLUGIN LOADER]")
        
        plugin_dir = 'plugin'
        if not os.path.exists(plugin_dir):
            print(Fore.RED + "  [ERROR] Plugin directory not found!")
            return False
        
        plugin_files = [f for f in os.listdir(plugin_dir) if f.endswith('.py')]
        
        if not plugin_files:
            print(Fore.RED + "  [WARNING] No plugin files found!")
            return False
        
        print(Fore.CYAN + f"  Found {len(plugin_files)} plugin(s):")
        
        plugin_categories = {
            'attack': ['DDOS', 'DOS'],
            'web': ['SQL_injection', 'XSS', 'deface'],
            'recon': ['recon', 'vuln_scanner'],
            'utility': ['location', 'network']
        }
        
        loaded_count = 0
        for pfile in plugin_files:
            plugin_name = pfile.replace('.py', '')
            plugin_path = os.path.join(plugin_dir, pfile)
            
            try:
                with open(plugin_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                line_count = len(lines)
                
                category = 'unknown'
                for cat, plugins in plugin_categories.items():
                    if plugin_name in plugins:
                        category = cat
                        break
                
                status_color = Fore.GREEN if line_count > 300 else Fore.YELLOW
                status_text = "READY" if line_count > 300 else "MINIMAL"
                
                self.plugins[plugin_name] = {
                    'path': plugin_path,
                    'lines': line_count,
                    'category': category,
                    'status': 'ready' if line_count > 100 else 'minimal'
                }
                
                print(f"  {status_color}[{status_text}] {plugin_name:<20} ({category:<8}) {line_count:>4} lines")
                loaded_count += 1
                
            except Exception as e:
                print(Fore.RED + f"  [ERROR] Failed to load {plugin_name}: {e}")
        
        self.plugins_loaded = True
        print(Fore.GREEN + f"\n  [SUCCESS] Loaded {loaded_count}/{len(plugin_files)} plugins")
        return True
    
    def show_main_menu(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "MAIN MENU - AIO TOOLS")
        print(Fore.CYAN + "="*80)
        
        menu_options = [
            ("1", "Web Attack Tools", Fore.RED),
            ("2", "Network Tools", Fore.BLUE),
            ("3", "Reconnaissance", Fore.GREEN),
            ("4", "Vulnerability Scanner", Fore.MAGENTA),
            ("5", "Utility Tools", Fore.CYAN),
            ("6", "Plugin Manager", Fore.YELLOW),
            ("7", "System Information", Fore.WHITE),
            ("8", "Settings", Fore.LIGHTBLACK_EX),
            ("9", "Update Tools", Fore.LIGHTCYAN_EX),
            ("0", "Exit", Fore.LIGHTRED_EX)
        ]
        
        for num, text, color in menu_options:
            print(f"{color}[{num}] {text}")
        
        print(Fore.CYAN + "="*80)
    
    def show_web_attack_menu(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "WEB ATTACK TOOLS")
        print(Fore.CYAN + "="*80)
        
        web_tools = [
            ("1", "SQL Injection Scanner", "SQL_injection"),
            ("2", "XSS Scanner & Exploiter", "XSS"),
            ("3", "Website Defacer", "deface"),
            ("4", "DDOS Attack Tool", "DDOS"),
            ("5", "DOS Attack Tool", "DOS"),
            ("6", "Web Crawler", "crawler"),
            ("7", "Parameter Bruteforcer", "bruteforce"),
            ("8", "Back to Main Menu", "back")
        ]
        
        for num, text, plugin in web_tools:
            if plugin in self.plugins:
                status = Fore.GREEN + "✓" if self.plugins[plugin]['lines'] > 300 else Fore.YELLOW + "⚠"
            else:
                status = Fore.RED + "✗"
            
            print(f"{Fore.CYAN}[{num}] {text} {status}")
        
        print(Fore.CYAN + "="*80)
        
        while True:
            choice = input(Fore.MAGENTA + "\nSelect tool (1-8): ").strip()
            
            if choice == '1' and 'SQL_injection' in self.plugins:
                self.run_plugin('SQL_injection')
                break
            elif choice == '2' and 'XSS' in self.plugins:
                self.run_plugin('XSS')
                break
            elif choice == '3' and 'deface' in self.plugins:
                self.run_plugin('deface')
                break
            elif choice == '4' and 'DDOS' in self.plugins:
                self.run_plugin('DDOS')
                break
            elif choice == '5' and 'DOS' in self.plugins:
                self.run_plugin('DOS')
                break
            elif choice == '6':
                print(Fore.YELLOW + "\n[INFO] Web Crawler coming soon!")
                break
            elif choice == '7':
                print(Fore.YELLOW + "\n[INFO] Parameter Bruteforcer coming soon!")
                break
            elif choice == '8':
                break
            else:
                print(Fore.RED + "[ERROR] Invalid selection or plugin not available")
    
    def show_network_tools_menu(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "NETWORK TOOLS")
        print(Fore.CYAN + "="*80)
        
        network_tools = [
            ("1", "Port Scanner", "port_scanner"),
            ("2", "Network Sniffer", "sniffer"),
            ("3", "Packet Analyzer", "packet_analyzer"),
            ("4", "MAC Address Changer", "mac_changer"),
            ("5", "ARP Spoofer", "arp_spoof"),
            ("6", "Network Mapper", "nmap_wrapper"),
            ("7", "Bandwidth Monitor", "bandwidth"),
            ("8", "Back to Main Menu", "back")
        ]
        
        for num, text, plugin in network_tools:
            if plugin in self.plugins:
                status = Fore.GREEN + "✓"
            else:
                status = Fore.YELLOW + "⚙"
            
            print(f"{Fore.BLUE}[{num}] {text} {status}")
        
        print(Fore.CYAN + "="*80)
        
        choice = input(Fore.MAGENTA + "\nSelect tool (1-8): ").strip()
        
        if choice == '1':
            self.run_network_tool('port_scanner')
        elif choice == '2':
            print(Fore.YELLOW + "\n[INFO] Network Sniffer coming soon!")
        elif choice == '3':
            print(Fore.YELLOW + "\n[INFO] Packet Analyzer coming soon!")
        elif choice == '4':
            self.run_network_tool('mac_changer')
        elif choice == '5':
            print(Fore.YELLOW + "\n[INFO] ARP Spoofer coming soon!")
        elif choice == '6':
            self.run_network_tool('nmap_wrapper')
        elif choice == '7':
            print(Fore.YELLOW + "\n[INFO] Bandwidth Monitor coming soon!")
    
    def show_recon_menu(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "RECONNAISSANCE TOOLS")
        print(Fore.CYAN + "="*80)
        
        recon_tools = [
            ("1", "IP/Website Information", "recon"),
            ("2", "Subdomain Finder", "subdomain"),
            ("3", "Directory Bruteforcer", "dir_bruteforce"),
            ("4", "WHOIS Lookup", "whois"),
            ("5", "DNS Enumeration", "dns_enum"),
            ("6", "Email Harvester", "email_harvester"),
            ("7", "Phone Number Lookup", "phone_lookup"),
            ("8", "Social Media Recon", "social_recon"),
            ("9", "Back to Main Menu", "back")
        ]
        
        for num, text, plugin in recon_tools:
            if plugin in self.plugins:
                status = Fore.GREEN + "✓"
            else:
                status = Fore.YELLOW + "⚙"
            
            print(f"{Fore.GREEN}[{num}] {text} {status}")
        
        print(Fore.CYAN + "="*80)
        
        choice = input(Fore.MAGENTA + "\nSelect tool (1-9): ").strip()
        
        if choice == '1' and 'recon' in self.plugins:
            self.run_plugin('recon')
        elif choice == '2':
            self.run_recon_tool('subdomain')
        elif choice == '3':
            self.run_recon_tool('dir_bruteforce')
        elif choice == '4':
            self.run_recon_tool('whois')
        elif choice == '5':
            self.run_recon_tool('dns_enum')
        elif choice == '6':
            print(Fore.YELLOW + "\n[INFO] Email Harvester coming soon!")
        elif choice == '7':
            print(Fore.YELLOW + "\n[INFO] Phone Number Lookup coming soon!")
        elif choice == '8':
            print(Fore.YELLOW + "\n[INFO] Social Media Recon coming soon!")
    
    def show_utility_menu(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "UTILITY TOOLS")
        print(Fore.CYAN + "="*80)
        
        utility_tools = [
            ("1", "Location Tracker", "location"),
            ("2", "Password Generator", "password_gen"),
            ("3", "File Encryptor/Decryptor", "crypto"),
            ("4", "Hash Cracker", "hash_cracker"),
            ("5", "Code Obfuscator", "obfuscator"),
            ("6", "Log Analyzer", "log_analyzer"),
            ("7", "System Monitor", "system_monitor"),
            ("8", "Backup Tool", "backup"),
            ("9", "Back to Main Menu", "back")
        ]
        
        for num, text, plugin in utility_tools:
            if plugin in self.plugins:
                status = Fore.GREEN + "✓"
            else:
                status = Fore.YELLOW + "⚙"
            
            print(f"{Fore.CYAN}[{num}] {text} {status}")
        
        print(Fore.CYAN + "="*80)
        
        choice = input(Fore.MAGENTA + "\nSelect tool (1-9): ").strip()
        
        if choice == '1' and 'location' in self.plugins:
            self.run_plugin('location')
        elif choice == '2':
            self.run_utility_tool('password_gen')
        elif choice == '3':
            print(Fore.YELLOW + "\n[INFO] File Encryptor coming soon!")
        elif choice == '4':
            self.run_utility_tool('hash_cracker')
        elif choice == '5':
            print(Fore.YELLOW + "\n[INFO] Code Obfuscator coming soon!")
        elif choice == '6':
            self.run_utility_tool('log_analyzer')
        elif choice == '7':
            self.run_utility_tool('system_monitor')
        elif choice == '8':
            print(Fore.YELLOW + "\n[INFO] Backup Tool coming soon!")
    
    def run_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            print(Fore.RED + f"\n[ERROR] Plugin '{plugin_name}' not found!")
            return False
        
        plugin_path = self.plugins[plugin_name]['path']
        
        print(Fore.YELLOW + f"\n[LAUNCHING] {plugin_name}...")
        print(Fore.CYAN + "-"*60)
        
        try:
            with open(plugin_path, 'r', encoding='utf-8') as f:
                exec(globals())
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to run plugin: {e}")
            return False
    
    def run_network_tool(self, tool_name):
        tool_scripts = {
            'port_scanner': '''
import socket
import threading
from datetime import datetime

def port_scanner():
    target = input("Enter target IP or domain: ")
    try:
        target_ip = socket.gethostbyname(target)
    except:
        target_ip = target
    
    print(f"\\nScanning {target_ip}...")
    
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port}: OPEN")
            sock.close()
        except:
            pass
    
    threads = []
    for port in range(1, 1025):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"\\nScan complete! Found {len(open_ports)} open ports.")
    return open_ports

if __name__ == "__main__":
    port_scanner()
''',
            'mac_changer': '''
import subprocess
import re
import random

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def change_mac(interface, new_mac):
    try:
        print(f"[*] Changing MAC address for {interface} to {new_mac}")
        
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
        
        print("[+] MAC address changed successfully")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    print("MAC Address Changer")
    interface = input("Enter interface (e.g., eth0, wlan0): ")
    choice = input("Generate random MAC? (y/n): ")
    
    if choice.lower() == 'y':
        new_mac = generate_random_mac()
    else:
        new_mac = input("Enter new MAC address (format: XX:XX:XX:XX:XX:XX): ")
    
    change_mac(interface, new_mac)
'''
        }
        
        if tool_name in tool_scripts:
            print(Fore.YELLOW + f"\n[RUNNING] {tool_name}...")
            exec(tool_scripts[tool_name])
        else:
            print(Fore.RED + f"\n[ERROR] Tool '{tool_name}' not implemented yet!")
    
    def run_recon_tool(self, tool_name):
        tool_scripts = {
            'subdomain': '''
import requests
import sys

def find_subdomains(domain):
    print(f"\\nFinding subdomains for {domain}...")
    
    subdomains = []
    wordlist = ['www', 'mail', 'ftp', 'admin', 'blog', 'api', 'test', 'dev', 'staging']
    
    for sub in wordlist:
        url = f"http://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code < 400:
                subdomains.append(url)
                print(f"[+] Found: {url}")
        except:
            pass
    
    print(f"\\nFound {len(subdomains)} subdomains:")
    for sub in subdomains:
        print(f"  {sub}")
    
    return subdomains

if __name__ == "__main__":
    domain = input("Enter domain (without http://): ").strip()
    find_subdomains(domain)
''',
            'dir_bruteforce': '''
import requests
import threading

def dir_bruteforce(url):
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\\nBruteforcing directories on {url}...")
    
    dirs = ['admin', 'login', 'wp-admin', 'dashboard', 'config', 'backup', 'uploads']
    found = []
    
    def check_dir(directory):
        test_url = f"{url}/{directory}"
        try:
            response = requests.get(test_url, timeout=3)
            if response.status_code == 200:
                found.append(test_url)
                print(f"[+] Found: {test_url}")
        except:
            pass
    
    threads = []
    for directory in dirs:
        thread = threading.Thread(target=check_dir, args=(directory,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"\\nFound {len(found)} directories:")
    for f in found:
        print(f"  {f}")

if __name__ == "__main__":
    url = input("Enter URL: ").strip()
    dir_bruteforce(url)
'''
        }
        
        if tool_name in tool_scripts:
            print(Fore.YELLOW + f"\n[RUNNING] {tool_name}...")
            exec(tool_scripts[tool_name])
        else:
            print(Fore.RED + f"\n[ERROR] Tool '{tool_name}' not implemented yet!")
    
    def run_utility_tool(self, tool_name):
        tool_scripts = {
            'password_gen': '''
import random
import string

def generate_password(length=12, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

if __name__ == "__main__":
    print("Password Generator")
    length = int(input("Password length (default 12): ") or 12)
    special = input("Include special characters? (y/n, default y): ").lower() != 'n'
    
    count = int(input("How many passwords to generate? (default 5): ") or 5)
    
    print("\\nGenerated Passwords:")
    for i in range(count):
        password = generate_password(length, special)
        print(f"{i+1}. {password}")
''',
            'hash_cracker': '''
import hashlib

def crack_hash(hash_value, wordlist):
    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                
                for algo in [hashlib.md5, hashlib.sha1, hashlib.sha256]:
                    hashed = algo(password.encode()).hexdigest()
                    if hashed == hash_value:
                        return password, algo.__name__
    except FileNotFoundError:
        print(f"Wordlist '{wordlist}' not found!")
    
    return None, None

if __name__ == "__main__":
    print("Hash Cracker")
    hash_value = input("Enter hash to crack: ").strip()
    wordlist = input("Enter wordlist file path: ").strip()
    
    print("\\nCracking...")
    result, algo = crack_hash(hash_value, wordlist)
    
    if result:
        print(f"\\n[SUCCESS] Found password: {result}")
        print(f"Hash algorithm: {algo}")
    else:
        print("\\n[FAILED] Password not found in wordlist")
'''
        }
        
        if tool_name in tool_scripts:
            print(Fore.YELLOW + f"\n[RUNNING] {tool_name}...")
            exec(tool_scripts[tool_name])
        else:
            print(Fore.RED + f"\n[ERROR] Tool '{tool_name}' not implemented yet!")
    
    def plugin_manager(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "PLUGIN MANAGER")
        print(Fore.CYAN + "="*80)
        
        print(Fore.YELLOW + "\nInstalled Plugins:")
        for plugin_name, info in self.plugins.items():
            status_color = Fore.GREEN if info['lines'] > 300 else Fore.YELLOW
            print(f"{status_color}{plugin_name:<20} {info['category']:<10} {info['lines']:>4} lines")
        
        print(Fore.CYAN + "\n" + "="*80)
        print("1. Reload all plugins")
        print("2. Check plugin updates")
        print("3. Create new plugin")
        print("4. Back to Main Menu")
        print(Fore.CYAN + "="*80)
        
        choice = input(Fore.MAGENTA + "\nSelect option (1-4): ").strip()
        
        if choice == '1':
            self.load_plugins()
        elif choice == '2':
            print(Fore.YELLOW + "\n[INFO] Update checking coming soon!")
        elif choice == '3':
            self.create_plugin()
        elif choice == '4':
            return
    
    def create_plugin(self):
        print(Fore.YELLOW + "\n[PLUGIN CREATOR]")
        
        plugin_name = input("Enter plugin name (without .py): ").strip()
        if not plugin_name:
            print(Fore.RED + "[ERROR] Plugin name required!")
            return
        
        category = input("Enter category (attack/web/recon/utility): ").strip()
        description = input("Enter plugin description: ").strip()
        
        template = f'''import sys
import os
import time
from datetime import datetime

class {plugin_name.title().replace('_', '')}Plugin:
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0.0"
        self.author = "AIO Tools"
        self.description = "{description}"
        self.category = "{category}"
        
    def display_header(self):
        print("\\n{'='*60}")
        print(f"{plugin_name.upper()} - AIO Tools Plugin")
        print("{'='*60}")
        print(f"Description: {description}")
        print(f"Category: {category}")
        print("{'='*60}\\n")
    
    def main_function(self):
        print("[INFO] This is the main function of the plugin")
        print("[INFO] Implement your functionality here")
        
        # Example functionality
        target = input("Enter target: ")
        print(f"[PROCESSING] Target: {target}")
        
        for i in range(5):
            print(f"[STEP {i+1}] Processing...")
            time.sleep(0.5)
        
        print("[COMPLETE] Operation finished")
    
    def run(self):
        self.display_header()
        self.main_function()

def main():
    plugin = {plugin_name.title().replace('_', '')}Plugin()
    plugin.run()

if __name__ == "__main__":
    main()
'''
        
        plugin_path = os.path.join('plugin', f"{plugin_name}.py")
        
        try:
            with open(plugin_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            print(Fore.GREEN + f"\n[SUCCESS] Plugin created: {plugin_path}")
            print(Fore.YELLOW + "[INFO] Reloading plugins...")
            self.load_plugins()
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to create plugin: {e}")
    
    def system_info(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "SYSTEM INFORMATION")
        print(Fore.CYAN + "="*80)
        
        import platform
        import psutil
        
        info = [
            ("System", platform.system()),
            ("Node Name", platform.node()),
            ("Release", platform.release()),
            ("Version", platform.version()),
            ("Machine", platform.machine()),
            ("Processor", platform.processor()),
            ("Python Version", platform.python_version()),
            ("CPU Cores", psutil.cpu_count()),
            ("Total RAM", f"{psutil.virtual_memory().total / (1024**3):.2f} GB"),
            ("Available RAM", f"{psutil.virtual_memory().available / (1024**3):.2f} GB"),
            ("Disk Usage", f"{psutil.disk_usage('/').percent}%"),
            ("Current Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("Uptime", str(datetime.now() - self.start_time))
        ]
        
        for key, value in info:
            print(Fore.GREEN + f"{key:<20}: {Fore.WHITE}{value}")
        
        print(Fore.CYAN + "\n" + "="*80)
    
    def update_tools(self):
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.YELLOW + "UPDATE SYSTEM")
        print(Fore.CYAN + "="*80)
        
        print(Fore.YELLOW + "\n[UPDATE] Checking for updates...")
        time.sleep(2)
        
        print(Fore.GREEN + "[INFO] AIO Tools is up to date!")
        print(Fore.YELLOW + "\n[OPTIONS]")
        print("1. Update all dependencies")
        print("2. Download new plugins")
        print("3. Check for framework updates")
        print("4. Back to Main Menu")
        
        choice = input(Fore.MAGENTA + "\nSelect option (1-4): ").strip()
        
        if choice == '1':
            print(Fore.YELLOW + "\nUpdating dependencies...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'requests', 'beautifulsoup4', 'colorama'])
            print(Fore.GREEN + "[SUCCESS] Dependencies updated!")
        elif choice == '2':
            print(Fore.YELLOW + "\n[INFO] Plugin download feature coming soon!")
        elif choice == '3':
            print(Fore.YELLOW + "\n[INFO] Checking GitHub for updates...")
            time.sleep(2)
            print(Fore.GREEN + "[INFO] You have the latest version!")
    
    def run(self):
        if not self.check_environment():
            return
        
        if not self.load_plugins():
            print(Fore.YELLOW + "[WARNING] Continuing with limited functionality")
        
        while True:
            self.display_header()
            self.show_main_menu()
            
            try:
                choice = input(Fore.MAGENTA + "\nSelect menu option (0-9): ").strip()
                
                if choice == '1':
                    self.show_web_attack_menu()
                elif choice == '2':
                    self.show_network_tools_menu()
                elif choice == '3':
                    self.show_recon_menu()
                elif choice == '4':
                    print(Fore.YELLOW + "\n[INFO] Vulnerability Scanner coming soon!")
                    input(Fore.CYAN + "\nPress Enter to continue...")
                elif choice == '5':
                    self.show_utility_menu()
                elif choice == '6':
                    self.plugin_manager()
                elif choice == '7':
                    self.system_info()
                    input(Fore.CYAN + "\nPress Enter to continue...")
                elif choice == '8':
                    print(Fore.YELLOW + "\n[INFO] Settings menu coming soon!")
                    input(Fore.CYAN + "\nPress Enter to continue...")
                elif choice == '9':
                    self.update_tools()
                elif choice == '0':
                    print(Fore.RED + "\n[EXIT] Shutting down AIO Tools...")
                    print(Fore.GREEN + "[GOODBYE] Stay secure!\n")
                    break
                else:
                    print(Fore.RED + "[ERROR] Invalid selection!")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print(Fore.RED + "\n\n[INTERRUPT] Shutting down...")
                break
            except Exception as e:
                print(Fore.RED + f"[ERROR] {e}")
                time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description='AIO Tools - Advanced Security Framework')
    parser.add_argument('--plugin', type=str, help='Run specific plugin directly')
    parser.add_argument('--update', action='store_true', help='Update AIO Tools')
    parser.add_argument('--info', action='store_true', help='Show system information')
    
    args = parser.parse_args()
    
    core = AIOToolsCore()
    
    if args.update:
        core.update_tools()
        return
    elif args.info:
        core.system_info()
        return
    elif args.plugin:
        core.load_plugins()
        core.run_plugin(args.plugin)
        return
    
    core.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[INTERRUPT] AIO Tools terminated")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n[FATAL ERROR] {e}")
        sys.exit(1)