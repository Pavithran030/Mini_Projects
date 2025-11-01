import requests
import re
import os
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from bs4 import BeautifulSoup

class XSSDetector:
    def __init__(self, session, delay=1, timeout=10):
        self.session = session
        self.delay = delay
        self.timeout = timeout

    def load_payloads(self, filepath='payloads/xss_payloads.txt'):
        try:
            # Try relative path first
            if not os.path.isabs(filepath):
                # Get the EH directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                eh_dir = os.path.dirname(current_dir)
                filepath = os.path.join(eh_dir, filepath)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            return [
                "<script>alert('xss_test')</script>",
                "<img src=x onerror=alert('xss_test')>",
                "'><script>alert('xss_test')</script>",
                "<svg onload=alert('xss_test')>"
            ]

    def test_url_params(self, url):
        findings = []
        parsed = urlparse(url)
        if not parsed.query:
            return findings

        base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        params = parse_qs(parsed.query, keep_blank_values=True)
        payloads = self.load_payloads()

        for param in params:
            for payload in payloads:
                try:
                    test_params = params.copy()
                    test_params[param] = [payload]
                    query = urlencode(test_params, doseq=True)
                    test_url = f"{base}?{query}"

                    resp = self.session.get(test_url, timeout=self.timeout)
                    if resp and payload in resp.text:
                        # Verify it's not inside a script tag or encoded
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        if soup.find(string=re.compile(re.escape(payload))):
                            findings.append({
                                'type': 'Reflected XSS',
                                'url': test_url,
                                'payload': payload,
                                'method': 'GET',
                                'evidence': payload[:50] + '...'
                            })
                    
                    # Add delay between requests
                    import time
                    time.sleep(self.delay)
                except requests.RequestException:
                    continue
        return findings

    def test_forms(self, url, html):
        from scanner.utils import extract_forms
        findings = []
        forms = extract_forms(html, url)
        payloads = self.load_payloads()

        for form in forms:
            for payload in payloads:
                data = {inp: payload for inp in form['inputs']}
                try:
                    if form['method'] == 'POST':
                        resp = self.session.post(form['action'], data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(form['action'], params=data, timeout=self.timeout)
                    
                    if resp and payload in resp.text:
                        findings.append({
                            'type': 'XSS in Form',
                            'url': form['action'],
                            'payload': payload,
                            'method': form['method'],
                            'evidence': payload[:50] + '...'
                        })
                except requests.RequestException:
                    continue
        return findings