import requests
import os
from colorama import Fore, Style
from scanner.sqli_detector import SQLInjectionDetector
from scanner.xss_detector import XSSDetector
from scanner.reporter import Reporter
from scanner.utils import validate_url, is_localhost

class VulnerabilityScanner:
    def __init__(self, target_url, delay=1, timeout=10, user_agent=None, output_dir=None, silent=False):
        if not validate_url(target_url):
            raise ValueError("URL must start with http:// or https://")

        self.target_url = target_url
        self.delay = delay
        self.timeout = timeout
        
        # Default to EH/reports folder if not specified
        if output_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            eh_parent = os.path.dirname(current_dir)  # Go up one level to EH folder
            self.output_dir = os.path.join(eh_parent, 'reports')
        else:
            self.output_dir = output_dir
            
        self.is_localhost = is_localhost(target_url)
        self.silent = silent

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'VulnScanner/1.0 (Educational Use Only)'
        })

        self.findings = []

    def run(self):
        if not self.silent:
            print(f"{Fore.YELLOW}🔒 Web Vulnerability Scanner (Educational Use Only)")
            print(f"{Fore.RED}⚠️  WARNING: Only scan systems you OWN or have explicit permission to test!")
            print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}")
            print(f"Target: {self.target_url}")
            
            if self.is_localhost:
                print(f"{Fore.GREEN}🏠 Localhost detected - Local testing mode{Style.RESET_ALL}")
            
            print(f"Delay: {self.delay}s | Timeout: {self.timeout}s\n")

        # Initial request to get base page
        try:
            resp = self.session.get(self.target_url, timeout=self.timeout)
            if not resp:
                if not self.silent:
                    print(f"{Fore.RED}❌ Failed to reach target URL.{Style.RESET_ALL}")
                return
        except requests.exceptions.Timeout:
            error_msg = f"Connection timed out after {self.timeout} seconds. Try increasing timeout with --timeout parameter."
            if not self.silent:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            raise TimeoutError(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection failed: {str(e)}"
            if not self.silent:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            raise ConnectionError(error_msg)
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            if not self.silent:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            raise

        # Run detectors
        sqli_detector = SQLInjectionDetector(self.session, self.delay, self.timeout)
        xss_detector = XSSDetector(self.session, self.delay, self.timeout)

        if not self.silent:
            print(f"{Fore.BLUE}🔍 Testing for SQL Injection...{Style.RESET_ALL}")
        self.findings.extend(sqli_detector.test_url_params(self.target_url))

        if not self.silent:
            print(f"{Fore.BLUE}🔍 Testing for XSS...{Style.RESET_ALL}")
        self.findings.extend(xss_detector.test_url_params(self.target_url))
        self.findings.extend(xss_detector.test_forms(self.target_url, resp.text))

        # Generate report
        reporter = Reporter(self.output_dir)
        if not self.silent:
            reporter.display_findings(self.findings)
        reporter.save_report(self.target_url, self.findings)