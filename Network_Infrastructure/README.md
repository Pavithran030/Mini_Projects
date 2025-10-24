# NetMap - Local Network Scanner

NetMap is a powerful yet easy-to-use local network scanner that discovers all active devices on your LAN and provides detailed information about each host.

## 🌟 Features

- **Automatic Network Detection**: Automatically detects your local IP address and subnet
- **ARP Scanning**: Fast discovery of live hosts using ARP protocol
- **Comprehensive Host Information**:
  - IP Address
  - MAC Address
  - Vendor identification (MAC OUI lookup)
  - Hostname (via reverse DNS/NetBIOS)
  - Port status for SSH (22), HTTP (80), and HTTPS (443)
- **Interactive Web UI**: Clean Streamlit interface with real-time scanning
- **CSV Export**: Export scan results to CSV for further analysis
- **Multi-threaded**: Fast scanning with concurrent host information gathering

## 📋 Prerequisites

- Python 3.8 or higher
- Administrator/Root privileges (required for ARP scanning)
- Windows, Linux, or macOS

## 🚀 Installation

1. **Clone or download the project**:
```powershell
cd "d:\Downloads\Mini Projectt\NI\NetMap"
```

2. **Create a virtual environment (recommended)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install required packages**:
```powershell
pip install -r requirements.txt
```

### Windows-Specific Requirements

On Windows, you'll also need to install:
- **Npcap** (for packet capture): Download from https://npcap.com/
  - During installation, make sure to check "Install Npcap in WinPcap API-compatible Mode"

## 💻 Usage

### Web UI (Recommended)

1. **Run the Streamlit application**:
```powershell
streamlit run app.py
```

2. **Open your browser** to the displayed URL (typically http://localhost:8501)

3. **Click "Detect Network"** to automatically detect your local network

4. **Click "Start Scan"** to begin scanning for devices

5. **View results** in the interactive table

6. **Export results** to CSV using the export button

### Command Line

You can also run the scanner directly from the command line:

```powershell
python network_scanner.py
```

This will perform a scan and print results to the console.

## 📁 Project Structure

```
NetMap/
├── app.py                  # Streamlit web interface
├── network_scanner.py      # Core scanning functionality
├── utils.py               # Utility functions (CSV export, etc.)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── exports/              # CSV export directory (created automatically)
```

## 🔧 How It Works

1. **Network Detection**: Uses `netifaces` to detect the default gateway interface and extract IP/subnet information

2. **ARP Scanning**: Sends ARP broadcast packets using `scapy` to discover all live hosts on the network

3. **Information Gathering**: For each discovered host:
   - MAC vendor lookup via macvendors.com API
   - Reverse DNS lookup for hostname
   - NetBIOS lookup (Windows networks) as fallback
   - TCP port scanning for common ports

4. **Results Display**: Shows all information in a clean, sortable table

## 🛡️ Security & Ethics

⚠️ **Important**: Only use NetMap on networks you own or have explicit permission to scan. Unauthorized network scanning may be illegal in your jurisdiction.

**Best Practices**:
- Always get permission before scanning
- Use on your home/test networks only
- Be aware of your organization's security policies
- This tool is for educational and legitimate network administration purposes only

## 🐛 Troubleshooting

### "No devices found"
- Make sure you're running with administrator/root privileges
- Check that Npcap is properly installed (Windows)
- Verify you're connected to the network

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment if using one

### Slow scanning
- Large networks (>50 hosts) may take several minutes
- You can reduce the scan time by scanning specific IP ranges

### Permission errors
- On Windows: Run PowerShell/CMD as Administrator
- On Linux/Mac: Use `sudo python app.py` or `sudo streamlit run app.py`

## 📊 Example Output

```
==================================================
IP Address      MAC Address        Vendor           Hostname        SSH     HTTP    HTTPS
==================================================
192.168.1.1     00:11:22:33:44:55  Cisco Systems   router          Closed  Open    Open
192.168.1.100   AA:BB:CC:DD:EE:FF  Apple Inc.      Johns-iPhone    Closed  Closed  Closed
192.168.1.150   11:22:33:44:55:66  Dell Inc.       DESKTOP-PC      Open    Open    Open
==================================================
```

## 🔄 Future Enhancements

- Advanced port scanning with customizable port ranges
- OS detection
- Service version detection
- Scheduled/automated scans
- Historical tracking of devices
- Network topology visualization
- Email alerts for new devices

## 📝 License

This project is provided for educational purposes. Use responsibly and ethically.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## ⚙️ Technical Details

**Dependencies**:
- `streamlit`: Web UI framework
- `scapy`: Packet manipulation and ARP scanning
- `netifaces`: Network interface information
- `pandas`: Data manipulation and display
- `requests`: HTTP requests for vendor lookup

**Protocols Used**:
- ARP (Address Resolution Protocol) for host discovery
- DNS for hostname resolution
- NetBIOS for Windows hostname lookup
- TCP for port scanning

## 📞 Support

If you encounter any issues or have questions, please create an issue in the repository.

---

**Happy Scanning! 🌐**
