"""
NetMap - Flask Web Application
Simple full-stack web interface for network scanning
"""

from flask import Flask, render_template, jsonify, request, send_file
from network_scanner import NetworkScanner
from utils import export_to_csv
import os
import threading

app = Flask(__name__, template_folder='ui', static_folder='ui')

# Global variables to store scan state
scan_status = {
    'scanning': False,
    'progress': 0,
    'message': '',
    'results': None,
    'local_ip': None,
    'subnet': None
}

scanner = NetworkScanner()


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/detect-network', methods=['GET'])
def detect_network():
    """Detect local network information"""
    try:
        local_ip, subnet = scanner.get_local_network_info()
        scan_status['local_ip'] = local_ip
        scan_status['subnet'] = subnet
        
        return jsonify({
            'success': True,
            'local_ip': local_ip,
            'subnet': subnet
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/start-scan', methods=['POST'])
def start_scan():
    """Start network scan in background thread"""
    if scan_status['scanning']:
        return jsonify({
            'success': False,
            'error': 'Scan already in progress'
        }), 400
    
    # Reset status
    scan_status['scanning'] = True
    scan_status['progress'] = 0
    scan_status['message'] = 'Initializing scan...'
    scan_status['results'] = None
    
    # Start scan in background thread
    thread = threading.Thread(target=perform_scan)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Scan started'
    })


def perform_scan():
    """Perform the actual network scan"""
    try:
        # Update progress
        scan_status['progress'] = 10
        scan_status['message'] = 'Detecting network...'
        
        # Detect network if not already done
        if not scanner.subnet:
            scanner.get_local_network_info()
            scan_status['local_ip'] = scanner.local_ip
            scan_status['subnet'] = scanner.subnet
        
        # Perform ARP scan
        scan_status['progress'] = 30
        scan_status['message'] = f'Scanning network {scanner.subnet}...'
        devices = scanner.perform_arp_scan()
        
        if not devices:
            scan_status['scanning'] = False
            scan_status['progress'] = 100
            scan_status['message'] = 'No devices found'
            return
        
        # Gather detailed information for discovered devices
        scan_status['progress'] = 60
        scan_status['message'] = f'Gathering information for {len(devices)} hosts...'
        
        # Use ThreadPoolExecutor to gather info from the devices we already found
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import ipaddress
        
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_device = {
                executor.submit(scanner.gather_host_info, device): device 
                for device in devices
            }
            
            completed = 0
            total = len(devices)
            for future in as_completed(future_to_device):
                try:
                    host_info = future.result()
                    results.append(host_info)
                    completed += 1
                    # Update progress
                    progress = 60 + int((completed / total) * 35)
                    scan_status['progress'] = progress
                    scan_status['message'] = f'Gathering information... ({completed}/{total} hosts)'
                except Exception as e:
                    print(f"Error gathering info: {e}")
        
        # Sort by IP address
        results.sort(key=lambda x: ipaddress.IPv4Address(x['IP Address']))
        
        # Complete
        scan_status['progress'] = 100
        scan_status['message'] = 'Scan complete!'
        scan_status['results'] = results
        scan_status['scanning'] = False
        
    except Exception as e:
        scan_status['scanning'] = False
        scan_status['progress'] = 0
        scan_status['message'] = f'Error: {str(e)}'
        scan_status['results'] = None


@app.route('/api/scan-status', methods=['GET'])
def get_scan_status():
    """Get current scan status"""
    return jsonify({
        'scanning': scan_status['scanning'],
        'progress': scan_status['progress'],
        'message': scan_status['message'],
        'local_ip': scan_status['local_ip'],
        'subnet': scan_status['subnet'],
        'has_results': scan_status['results'] is not None
    })


@app.route('/api/results', methods=['GET'])
def get_results():
    """Get scan results"""
    if scan_status['results'] is None:
        return jsonify({
            'success': False,
            'error': 'No scan results available'
        }), 404
    
    # Calculate statistics
    total_hosts = len(scan_status['results'])
    ssh_open = sum(1 for h in scan_status['results'] if h['SSH (22)'] == 'Open')
    http_open = sum(1 for h in scan_status['results'] if h['HTTP (80)'] == 'Open')
    https_open = sum(1 for h in scan_status['results'] if h['HTTPS (443)'] == 'Open')
    
    return jsonify({
        'success': True,
        'results': scan_status['results'],
        'statistics': {
            'total_hosts': total_hosts,
            'ssh_open': ssh_open,
            'http_open': http_open,
            'https_open': https_open
        }
    })


@app.route('/api/export', methods=['POST'])
def export_results():
    """Export scan results to CSV"""
    if scan_status['results'] is None:
        return jsonify({
            'success': False,
            'error': 'No scan results to export'
        }), 404
    
    try:
        data = request.json
        filename = data.get('filename', None) if data else None
        
        filepath = export_to_csv(scan_status['results'], filename)
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'filename': os.path.basename(filepath)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download exported CSV file"""
    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
    filepath = os.path.join(exports_dir, filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404


@app.route('/favicon.ico')
def favicon():
    """Return empty response for favicon requests to avoid 404 in logs"""
    # If you want a real favicon, place it under the static folder (ui/favicon.ico)
    return ('', 204)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  NetMap - Network Scanner Web Application")
    print("="*60)
    print("\n  Starting server...")
    print("  Open your browser to: http://localhost:5000")
    print("\n  Press Ctrl+C to stop\n")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
