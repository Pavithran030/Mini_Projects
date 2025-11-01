import argparse
import sys
import os
from colorama import init
from scanner.core import VulnerabilityScanner

# Initialize colorama for Windows compatibility
init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(
        description="Automated Web Vulnerability Scanner (SQLi & XSS)",
        epilog="⚠️  For educational and authorized testing ONLY."
    )
    parser.add_argument('url', help='Target URL to scan (e.g., http://localhost:8080 or https://example.com)')
    parser.add_argument('--delay', type=float, default=1.0,
                        help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--timeout', type=int, default=20,
                        help='Request timeout in seconds (default: 10)')
    parser.add_argument('--user-agent', type=str,
                        help='Custom User-Agent string')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Directory to save reports (default: EH/reports)')

    args = parser.parse_args()

    try:
        scanner = VulnerabilityScanner(
            target_url=args.url,
            delay=args.delay,
            timeout=args.timeout,
            user_agent=args.user_agent,
            output_dir=args.output_dir
        )
        scanner.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Scan interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()