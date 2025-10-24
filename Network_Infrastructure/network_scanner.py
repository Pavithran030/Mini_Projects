"""
NetMap - Network Scanner Core Module
Discovers active devices on local network and collects host information
"""

import socket
import ipaddress
import netifaces
from scapy.all import ARP, Ether, srp
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time


class NetworkScanner:
    """Main network scanner class for discovering and analyzing hosts"""
    
    def __init__(self):
        self.local_ip = None
        self.subnet = None
        self.hosts = []
        
    def get_local_network_info(self):
        """
        Automatically detect local IP address and subnet
        Returns: tuple (local_ip, subnet)
        """
        try:
            # Get default gateway interface
            gateways = netifaces.gateways()
            default_interface = gateways['default'][netifaces.AF_INET][1]
            
            # Get IP address and netmask for the interface
            addrs = netifaces.ifaddresses(default_interface)
            ipinfo = addrs[netifaces.AF_INET][0]
            
            self.local_ip = ipinfo['addr']
            netmask = ipinfo['netmask']
            
            # Calculate network address and CIDR
            network = ipaddress.IPv4Network(f"{self.local_ip}/{netmask}", strict=False)
            self.subnet = str(network)
            
            return self.local_ip, self.subnet
            
        except Exception as e:
            print(f"Error detecting network: {e}")
            # Fallback method
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                self.local_ip = s.getsockname()[0]
                # Assume /24 subnet as fallback
                ip_parts = self.local_ip.split('.')
                self.subnet = f"{'.'.join(ip_parts[:3])}.0/24"
            finally:
                s.close()
            
            return self.local_ip, self.subnet
    
    def perform_arp_scan(self, subnet=None):
        """
        Perform ARP scan to discover live hosts
        Args:
            subnet: Network subnet to scan (e.g., '192.168.1.0/24')
        Returns:
            list of dicts with IP and MAC addresses
        """
        if subnet is None:
            subnet = self.subnet
        
        print(f"[*] Scanning network: {subnet}")
        
        try:
            # Create ARP request packet
            arp = ARP(pdst=subnet)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            # Send packet and receive response
            result = srp(packet, timeout=3, verbose=0)[0]
            
            # Parse responses
            devices = []
            for sent, received in result:
                devices.append({
                    'ip': received.psrc,
                    'mac': received.hwsrc
                })
            
            print(f"[+] Found {len(devices)} active hosts")
            return devices
            
        except Exception as e:
            print(f"Error performing ARP scan: {e}")
            return []
    
    def get_mac_vendor(self, mac_address):
        """
        Lookup MAC vendor using MAC OUI database
        Args:
            mac_address: MAC address string
        Returns:
            Vendor name or 'Unknown'
        """
        try:
            # Format MAC for API (remove colons/dashes)
            mac_clean = mac_address.replace(':', '').replace('-', '')
            
            # Use macvendors.com API
            url = f"https://api.macvendors.com/{mac_address}"
            response = requests.get(url, timeout=2)
            
            if response.status_code == 200:
                return response.text
            else:
                return "Unknown"
                
        except Exception as e:
            return "Unknown"
    
    def get_hostname(self, ip_address):
        """
        Get hostname via reverse DNS lookup
        Args:
            ip_address: IP address string
        Returns:
            Hostname or 'N/A'
        """
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except:
            # Try NetBIOS if DNS fails (Windows networks)
            try:
                import subprocess
                result = subprocess.run(
                    ['nbtstat', '-A', ip_address],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                # Parse NetBIOS name from output
                for line in result.stdout.split('\n'):
                    if '<00>' in line and 'UNIQUE' in line:
                        name = line.split()[0].strip()
                        if name and not name.startswith('MAC'):
                            return name
            except:
                pass
            
            return "N/A"
    
    def check_port(self, ip, port, timeout=1):
        """
        Check if a specific port is open on a host
        Args:
            ip: IP address
            port: Port number
            timeout: Connection timeout in seconds
        Returns:
            bool: True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_common_ports(self, ip):
        """
        Check common ports (22, 80, 443) for a host
        Args:
            ip: IP address
        Returns:
            dict with port status
        """
        ports = {
            22: 'SSH',
            80: 'HTTP',
            443: 'HTTPS'
        }
        
        port_status = {}
        for port, service in ports.items():
            is_open = self.check_port(ip, port)
            port_status[service] = 'Open' if is_open else 'Closed'
        
        return port_status
    
    def gather_host_info(self, device):
        """
        Gather complete information for a single host
        Args:
            device: dict with 'ip' and 'mac' keys
        Returns:
            dict with complete host information
        """
        ip = device['ip']
        mac = device['mac']
        
        print(f"[*] Gathering info for {ip}")
        
        # Get vendor
        vendor = self.get_mac_vendor(mac)
        
        # Small delay to avoid rate limiting
        time.sleep(0.3)
        
        # Get hostname
        hostname = self.get_hostname(ip)
        
        # Check ports
        port_status = self.check_common_ports(ip)
        
        return {
            'IP Address': ip,
            'MAC Address': mac,
            'Vendor': vendor,
            'Hostname': hostname,
            'SSH (22)': port_status['SSH'],
            'HTTP (80)': port_status['HTTP'],
            'HTTPS (443)': port_status['HTTPS']
        }
    
    def scan_network(self, max_workers=10):
        """
        Perform complete network scan
        Args:
            max_workers: Number of concurrent threads for info gathering
        Returns:
            list of dicts with complete host information
        """
        # Detect network
        print("[*] Detecting local network...")
        self.get_local_network_info()
        print(f"[+] Local IP: {self.local_ip}")
        print(f"[+] Subnet: {self.subnet}")
        
        # Perform ARP scan
        devices = self.perform_arp_scan()
        
        if not devices:
            print("[-] No devices found")
            return []
        
        # Gather detailed information for each host
        print(f"\n[*] Gathering detailed information for {len(devices)} hosts...")
        self.hosts = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_device = {
                executor.submit(self.gather_host_info, device): device 
                for device in devices
            }
            
            for future in as_completed(future_to_device):
                try:
                    host_info = future.result()
                    self.hosts.append(host_info)
                except Exception as e:
                    print(f"Error gathering info: {e}")
        
        # Sort by IP address
        self.hosts.sort(key=lambda x: ipaddress.IPv4Address(x['IP Address']))
        
        print(f"\n[+] Scan complete! Found {len(self.hosts)} hosts")
        return self.hosts
    
    def print_results(self):
        """Print scan results in a formatted table"""
        if not self.hosts:
            print("No hosts to display")
            return
        
        # Print header
        print("\n" + "="*120)
        print(f"{'IP Address':<15} {'MAC Address':<18} {'Vendor':<25} {'Hostname':<20} {'SSH':<8} {'HTTP':<8} {'HTTPS':<8}")
        print("="*120)
        
        # Print each host
        for host in self.hosts:
            print(f"{host['IP Address']:<15} "
                  f"{host['MAC Address']:<18} "
                  f"{host['Vendor'][:24]:<25} "
                  f"{host['Hostname'][:19]:<20} "
                  f"{host['SSH (22)']:<8} "
                  f"{host['HTTP (80)']:<8} "
                  f"{host['HTTPS (443)']:<8}")
        
        print("="*120)


if __name__ == "__main__":
    scanner = NetworkScanner()
    scanner.scan_network()
    scanner.print_results()
