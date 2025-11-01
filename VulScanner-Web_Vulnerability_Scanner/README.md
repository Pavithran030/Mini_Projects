# EH Vulnerability Scanner - README

## 🔒 Overview

**EH (Ethical Hacking) Vulnerability Scanner** is an educational web security tool designed to detect common vulnerabilities in web applications. It focuses on two major vulnerability types:
- **SQL Injection (SQLi)**
- **Cross-Site Scripting (XSS)**

⚠️ **EDUCATIONAL PURPOSE ONLY** - Use only on systems you own or have explicit permission to test.

---

## ✨ Features

### Core Features
- 🔍 **Automated SQL Injection Detection** - Tests URL parameters and forms
- 🎯 **XSS Vulnerability Detection** - Reflected and stored XSS testing
- 📊 **Detailed Reporting** - JSON reports with full vulnerability details
- 🌐 **Web Interface** - User-friendly Flask-based UI
- 💻 **CLI Interface** - Command-line tool for quick scans
- 🎨 **Color-Coded Output** - Easy-to-read terminal output
- 🔄 **Configurable Scanning** - Adjustable delays, timeouts, and payloads

### Technical Features
- Multi-threaded scanning for efficiency
- Custom payload support
- User-Agent customization
- Localhost detection for safe testing
- Request/response analysis
- HTTP method testing (GET/POST)
- Form field discovery and testing

---

## 📋 Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)
- **Internet connection** (for scanning remote targets)

---

## 🚀 Installation

### 1. Navigate to EH Directory
```powershell
cd "d:\Downloads\Mini Projectt\EH"
```

### 2. Create Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 💻 Usage

### Option 1: Web Interface (Recommended)

```powershell
python app.py
```

Then open your browser to: **http://localhost:5000**

**Features:**
- Enter target URL
- Configure scan parameters
- Start scan with one click
- View results in real-time
- Access previous scan reports

### Option 2: Command Line Interface

**Basic Scan:**
```powershell
python main.py http://testphp.vulnweb.com
```

**Advanced Options:**
```powershell
# Custom delay between requests
python main.py http://target.com --delay 2.0

# Custom timeout
python main.py http://target.com --timeout 30

# Custom User-Agent
python main.py http://target.com --user-agent "Mozilla/5.0..."

# Custom output directory
python main.py http://target.com --output-dir ./my_reports
```

**Help:**
```powershell
python main.py --help
```

---

## 📁 Project Structure

```
EH/
├── app.py                     # Flask web application
├── main.py                    # Command-line interface
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
│
├── scanner/                   # Core scanner modules
│   ├── __init__.py
│   ├── core.py               # Main scanner logic
│   ├── reporter.py           # Report generation
│   ├── sqli_detector.py      # SQL Injection detector
│   ├── xss_detector.py       # XSS detector
│   └── utils.py              # Utility functions
│
├── templates/                 # Web UI templates
│   └── index.html            # Main web interface
│
├── payloads/                  # Attack payloads
│   ├── sqli_payloads.txt     # SQL injection payloads
│   └── xss_payloads.txt      # XSS payloads
│
├── reports/                   # Scan reports (auto-generated)
│   └── vuln_report_*.json    # JSON report files
│
└── docs/                      # Documentation
    ├── README.md             # This file
    ├── WEB_UI_GUIDE.txt      # Web UI guide
    └── GIT_PUSH_GUIDE.md     # Git instructions
```

---

## 🔬 How It Works

### SQL Injection Detection
1. Discovers URL parameters and form inputs
2. Injects SQL payloads (e.g., `' OR '1'='1`)
3. Analyzes responses for SQL error messages
4. Reports confirmed vulnerabilities

### XSS Detection
1. Identifies input fields and URL parameters
2. Injects XSS payloads (e.g., `<script>alert(1)</script>`)
3. Checks if payload is reflected in response
4. Tests different encoding methods
5. Reports successful XSS injections

---

## 📊 Report Format

Reports are saved in `reports/` directory as JSON files:

**Filename Format:** `vuln_report_YYYYMMDD_HHMMSS.json`

**Report Contents:**
```json
{
  "target_url": "http://example.com",
  "scan_time": "2025-10-23T16:30:00",
  "vulnerabilities_found": 2,
  "findings": [
    {
      "type": "SQL Injection",
      "url": "http://example.com/page?id=1",
      "method": "GET",
      "payload": "' OR '1'='1",
      "evidence": "SQL syntax error..."
    }
  ]
}
```

---

## ⚙️ Configuration

### Custom Payloads

Edit payload files in `payloads/` directory:
- `sqli_payloads.txt` - SQL injection payloads
- `xss_payloads.txt` - XSS payloads

Format: One payload per line

### Scan Parameters

**Delay:** Time between requests (seconds)
- Default: 1.0
- Recommended: 1-3 seconds to avoid rate limiting

**Timeout:** Request timeout (seconds)
- Default: 20
- Increase for slow servers

---

## 🛡️ Security & Ethics

### ⚠️ IMPORTANT WARNINGS

**ONLY scan systems where you have:**
- ✅ Explicit written permission from the owner
- ✅ Legal authorization to perform security testing
- ✅ Proper scope and rules of engagement

**NEVER scan:**
- ❌ Production systems without permission
- ❌ Third-party websites without authorization
- ❌ Government or military systems
- ❌ Any system you don't own

**Legal Note:** Unauthorized security testing may be illegal in your jurisdiction and could result in:
- Criminal charges
- Civil lawsuits
- Fines and penalties
- Imprisonment

### Safe Testing Environments

**Recommended Test Targets:**
- 🏠 Your own local applications
- 🧪 DVWA (Damn Vulnerable Web Application)
- 🎯 WebGoat (OWASP training platform)
- 🔬 http://testphp.vulnweb.com (Acunetix test site)
- 🌐 bWAPP (Buggy Web Application)

---

## 🐛 Troubleshooting

### Import Errors
```powershell
# Solution: Install dependencies
pip install -r requirements.txt
```

### Connection Errors
```powershell
# Solution: Check URL format
# Must include http:// or https://
python main.py https://example.com
```

### No Vulnerabilities Found
- Target may be properly secured (good!)
- Check if URL is accessible
- Try adjusting timeout for slow servers
- Verify target has testable parameters

### Permission Errors (Reports)
```powershell
# Solution: Check directory permissions
# Reports directory is created automatically
```

---

## 📚 Dependencies

- **Flask** - Web framework for UI
- **Requests** - HTTP library
- **BeautifulSoup4** - HTML parsing
- **Colorama** - Colored terminal output

See `requirements.txt` for versions.

---

## 🔄 Updates & Maintenance

### Check for Updates
```powershell
pip list --outdated
```

### Update Dependencies
```powershell
pip install --upgrade -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional vulnerability types (CSRF, LFI, RFI, etc.)
- Enhanced detection algorithms
- Better reporting formats (HTML, PDF)
- Performance optimizations
- Extended payload libraries

---

## 📝 License

This project is for **educational purposes only**. Use responsibly and ethically.

---

## 🆘 Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Test in safe environment first

---

## 🎓 Learning Resources

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **SQL Injection:** https://owasp.org/www-community/attacks/SQL_Injection
- **XSS:** https://owasp.org/www-community/attacks/xss/
- **Web Security Academy:** https://portswigger.net/web-security

---

## ✅ Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Virtual environment activated (optional but recommended)
- [ ] Permission obtained for target system
- [ ] Test on safe/authorized targets only
- [ ] Review legal implications in your jurisdiction

---

## 🎯 Example Workflow

```powershell
# 1. Setup
cd "d:\Downloads\Mini Projectt\EH"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Scan a test site
python main.py http://testphp.vulnweb.com --delay 2.0

# 3. View report
ls reports/
# Open the latest JSON file

# 4. Use Web UI
python app.py
# Open http://localhost:5000
```

---

**Remember: Use this tool responsibly and ethically! 🔒**

**For Educational and Authorized Testing Only!**
