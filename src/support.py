import json
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
    
    @staticmethod
    def calculate_md5(data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def calculate_sha256(data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def base64_encode(data):
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(data).decode()
    
    @staticmethod
    def base64_decode(data):
        try:
            return base64.b64decode(data).decode()
        except:
            return None
    
    @staticmethod
    def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def generate_random_ip():
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    @staticmethod
    def generate_user_agent():
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 13; Mobile) AppleWebKit/537.36'
        ]
        return random.choice(agents)
    
    @staticmethod
    def format_bytes(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_iso_timestamp():
        return datetime.now().isoformat()
    
    @staticmethod
    def parse_time_string(time_str):
        try:
            if 'd' in time_str:
                days = int(time_str.replace('d', ''))
                return timedelta(days=days)
            elif 'h' in time_str:
                hours = int(time_str.replace('h', ''))
                return timedelta(hours=hours)
            elif 'm' in time_str:
                minutes = int(time_str.replace('m', ''))
                return timedelta(minutes=minutes)
            elif 's' in time_str:
                seconds = int(time_str.replace('s', ''))
                return timedelta(seconds=seconds)
            else:
                seconds = int(time_str)
                return timedelta(seconds=seconds)
        except:
            return timedelta(seconds=30)
    
    @staticmethod
    def validate_ip_address(ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    
    @staticmethod
    def validate_port(port):
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except:
            return False
    
    @staticmethod
    def create_progress_bar(progress, width=50):
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {progress*100:.1f}%"

class FileHandler:
    @staticmethod
    def save_to_json(data, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
    
    @staticmethod
    def load_from_json(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    @staticmethod
    def append_to_log(log_file, message):
        try:
            timestamp = SupportUtils.get_timestamp()
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {message}\n")
            return True
        except:
            return False
    
    @staticmethod
    def read_last_lines(filename, num_lines=10):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-num_lines:] if lines else []
        except:
            return []

class NetworkValidator:
    @staticmethod
    def is_valid_url(url):
        import re
        pattern = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return pattern.match(url) is not None
    
    @staticmethod
    def extract_domain(url):
        import re
        pattern = r'^(?:https?://)?(?:www\.)?([^:/]+)'
        match = re.match(pattern, url)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_ip_from_string(text):
        import re
        pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        matches = re.findall(pattern, text)
        return matches if matches else []

class SecurityTools:
    @staticmethod
    def generate_password(length=12):
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        password = [
            random.choice(upper),
            random.choice(lower),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        all_chars = upper + lower + digits + symbols
        password += [random.choice(all_chars) for _ in range(length - 4)]
        
        random.shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def check_password_strength(password):
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            score += 1
        
        strength_levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong']
        return strength_levels[min(score, len(strength_levels)-1)]
    
    @staticmethod
    def encrypt_caesar(text, shift=3):
        result = ''
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    @staticmethod
    def decrypt_caesar(text, shift=3):
        return SecurityTools.encrypt_caesar(text, -shift)

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.operations = 0
    
    def increment_operations(self, count=1):
        self.operations += count
    
    def get_stats(self):
        elapsed = time.time() - self.start_time
        ops_per_sec = self.operations / elapsed if elapsed > 0 else 0
        return {
            'elapsed_time': elapsed,
            'total_operations': self.operations,
            'operations_per_second': ops_per_sec
        }
    
    def reset(self):
        self.start_time = time.time()
        self.operations = 0

if __name__ == "__main__":
    utils = SupportUtils()
    print(f"Session ID: {utils.generate_session_id()}")
    print(f"Random String: {utils.generate_random_string(20)}")
    print(f"MD5 of 'test': {utils.calculate_md5('test')}")
    print(f"Formatted Bytes: {utils.format_bytes(15443212)}")
    print(f"Current Timestamp: {utils.get_timestamp()}")