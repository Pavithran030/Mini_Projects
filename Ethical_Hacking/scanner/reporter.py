import json
import os
from datetime import datetime
from colorama import Fore, Style

class Reporter:
    def __init__(self, output_dir=None):
        # Default to EH/reports folder
        if output_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            eh_parent = os.path.dirname(current_dir)  # Go up one level to EH folder
            output_dir = os.path.join(eh_parent, 'reports')
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def display_findings(self, findings):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}SCAN COMPLETE – VULNERABILITY REPORT")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

        if not findings:
            print(f"{Fore.GREEN}✅ No vulnerabilities detected.{Style.RESET_ALL}")
            return

        for f in findings:
            print(f"\n{Fore.RED}🚨 {f['type']}{Style.RESET_ALL}")
            print(f"   {Fore.WHITE}URL:{Style.RESET_ALL} {f['url']}")
            print(f"   {Fore.WHITE}Method:{Style.RESET_ALL} {f['method']}")
            print(f"   {Fore.WHITE}Payload:{Style.RESET_ALL} {f['payload']}")
            print(f"   {Fore.WHITE}Evidence:{Style.RESET_ALL} {f.get('evidence', 'N/A')}")

    def save_report(self, target_url, findings):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vuln_report_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        report = {
            'target_url': target_url,
            'scan_time': datetime.now().isoformat(),
            'vulnerabilities_found': len(findings),
            'findings': findings
        }

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n{Fore.GREEN}📄 Report saved to: {filepath}{Style.RESET_ALL}")
        return filepath