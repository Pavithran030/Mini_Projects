import re
import requests
import os
from urllib.parse import urlparse, parse_qs, urlencode

class SQLInjectionDetector:
    def __init__(self, session, delay=1, timeout=10):
        self.session = session
        self.delay = delay
        self.timeout = timeout
        self.sql_errors = [
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"SQL syntax.*MariaDB",
            r"PostgreSQL.*ERROR",
            r"ORA-[0-9]{5}",
            r"SQLite.*error",
            r"Microsoft SQL Server.*[0-9a-fA-F]{8}",
            r"Unclosed quotation mark",
            r"quoted string not properly terminated"
        ]

    def load_payloads(self, filepath='payloads/sqli_payloads.txt'):
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
            # Fallback payloads
            return ["'", "\"", "1' OR '1'='1", "1' OR '1'='1' --", "' OR '1'='1' #"]

    def _has_sql_error(self, text):
        for pattern in self.sql_errors:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

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
                    if resp and self._has_sql_error(resp.text):
                        findings.append({
                            'type': 'SQL Injection',
                            'url': test_url,
                            'payload': payload,
                            'method': 'GET',
                            'evidence': 'SQL error message detected'
                        })
                    
                    # Add delay between requests
                    import time
                    time.sleep(self.delay)
                except requests.RequestException:
                    continue
        return findings