"""
NetMap - Utility Functions
Helper functions for CSV export and data formatting
"""

import csv
import os
from datetime import datetime


def export_to_csv(hosts, filename=None):
    """
    Export scan results to CSV file
    Args:
        hosts: List of host dictionaries
        filename: Output filename (optional, auto-generated if None)
    Returns:
        str: Path to saved CSV file
    """
    if not hosts:
        return None
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"netmap_scan_{timestamp}.csv"
    
    # Ensure .csv extension
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    # Create exports directory if it doesn't exist
    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
    os.makedirs(exports_dir, exist_ok=True)
    
    filepath = os.path.join(exports_dir, filename)
    
    # Write to CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'IP Address', 
            'MAC Address', 
            'Vendor', 
            'Hostname',
            'SSH (22)',
            'HTTP (80)',
            'HTTPS (443)'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(hosts)
    
    return filepath


def format_port_status(status):
    """
    Format port status with color indicators
    Args:
        status: 'Open' or 'Closed'
    Returns:
        Formatted string
    """
    if status == 'Open':
        return "🟢 Open"
    else:
        return "🔴 Closed"


def validate_ip(ip_string):
    """
    Validate IP address format
    Args:
        ip_string: IP address string
    Returns:
        bool: True if valid
    """
    import ipaddress
    try:
        ipaddress.IPv4Address(ip_string)
        return True
    except:
        return False


def validate_subnet(subnet_string):
    """
    Validate subnet/CIDR format
    Args:
        subnet_string: Subnet string (e.g., '192.168.1.0/24')
    Returns:
        bool: True if valid
    """
    import ipaddress
    try:
        ipaddress.IPv4Network(subnet_string, strict=False)
        return True
    except:
        return False
