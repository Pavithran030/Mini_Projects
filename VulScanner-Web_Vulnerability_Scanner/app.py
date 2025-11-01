from flask import Flask, render_template, request, jsonify
import sys
import os
from datetime import datetime
import json

# Add the scanner module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner.core import VulnerabilityScanner

app = Flask(__name__, template_folder='ui')

@app.route('/')
def index():
    """Render the main UI page"""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    """Handle scan requests"""
    try:
        data = request.get_json()
        target_url = data.get('url', '').strip()
        
        if not target_url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Get optional parameters
        delay = float(data.get('delay', 1.0))
        timeout = int(data.get('timeout', 20))
        
        # Get the EH/reports directory (we're already in EH folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(current_dir, 'reports')
        
        # Create scanner instance (silent mode for web UI)
        scanner = VulnerabilityScanner(
            target_url=target_url,
            delay=delay,
            timeout=timeout,
            output_dir=reports_dir,
            silent=True
        )
        
        # Run the scan
        scanner.run()
        
        # Get the findings
        findings = scanner.findings
        
        # Prepare response
        response = {
            'success': True,
            'target_url': target_url,
            'scan_time': datetime.now().isoformat(),
            'vulnerabilities_found': len(findings),
            'findings': findings,
            'is_localhost': scanner.is_localhost
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except TimeoutError as e:
        return jsonify({
            'success': False,
            'error': f'Connection timeout: {str(e)}'
        }), 408
    except ConnectionError as e:
        return jsonify({
            'success': False,
            'error': f'Connection failed: {str(e)}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Scan failed: {str(e)}'
        }), 500

@app.route('/reports')
def get_reports():
    """Get list of previous scan reports"""
    try:
        # Get the EH/reports directory (we're already in EH folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(current_dir, 'reports')
        
        if not os.path.exists(reports_dir):
            return jsonify({'reports': []})
        
        report_files = []
        for filename in os.listdir(reports_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(reports_dir, filename)
                with open(filepath, 'r') as f:
                    report_data = json.load(f)
                    report_files.append({
                        'filename': filename,
                        'target_url': report_data.get('target_url'),
                        'scan_time': report_data.get('scan_time'),
                        'vulnerabilities_found': report_data.get('vulnerabilities_found', 0)
                    })
        
        # Sort by scan time, newest first
        report_files.sort(key=lambda x: x['scan_time'], reverse=True)
        
        return jsonify({'reports': report_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create reports directory if it doesn't exist
    os.makedirs('./reports', exist_ok=True)
    
    print("=" * 60)
    print("🔒 Web Vulnerability Scanner - Web Interface")
    print("=" * 60)
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
