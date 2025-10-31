"""
NetMap CLI - Command Line Interface
Simple command-line interface for quick scans
"""

import argparse
from network_scanner import NetworkScanner
from utils import export_to_csv


def main():
    parser = argparse.ArgumentParser(
        description='NetMap - Local Network Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py                    # Scan local network
  python cli.py --export           # Scan and export to CSV
  python cli.py --subnet 192.168.1.0/24  # Scan specific subnet
  python cli.py --workers 20       # Use 20 concurrent threads
        """
    )
    
    parser.add_argument(
        '--subnet',
        help='Subnet to scan (e.g., 192.168.1.0/24). Auto-detected if not specified.',
        default=None
    )
    
    parser.add_argument(
        '--export',
        help='Export results to CSV',
        action='store_true'
    )
    
    parser.add_argument(
        '--output',
        help='Output CSV filename',
        default=None
    )
    
    parser.add_argument(
        '--workers',
        help='Number of concurrent threads (default: 10)',
        type=int,
        default=10
    )
    
    args = parser.parse_args()
    
    # Banner
    print("\n" + "="*60)
    print("  NetMap - Local Network Scanner v1.0")
    print("="*60 + "\n")
    
    # Initialize scanner
    scanner = NetworkScanner()
    
    # If subnet is specified, set it manually
    if args.subnet:
        scanner.subnet = args.subnet
        print(f"[*] Using specified subnet: {args.subnet}\n")
    
    # Perform scan
    try:
        results = scanner.scan_network(max_workers=args.workers)
        
        if results:
            # Print results
            scanner.print_results()
            
            # Export if requested
            if args.export:
                print("\n[*] Exporting results to CSV...")
                filepath = export_to_csv(results, args.output)
                print(f"[+] Results exported to: {filepath}")
        else:
            print("\n[-] No devices found on the network")
            print("[!] Make sure you're running with administrator/root privileges")
    
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("[!] Make sure you're running with administrator/root privileges")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
