# AIO TOOLS - Advanced Security Framework

A comprehensive, all-in-one security testing and penetration testing toolkit built with Python. Designed for security professionals, ethical hackers, and cybersecurity enthusiasts.

![AIO Tools Banner](https://img.shields.io/badge/AIO%20Tools-Advanced%20Security%20Framework-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![Platform](https://img.shields.io/badge/Platform-Windows%2FLinux%2FmacOS%2FTermux-lightgrey)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red)

## 🚀 Features

### 🛡️ Web Security Tools
- **SQL Injection Scanner** - Advanced SQLi detection with multiple techniques
- **XSS Vulnerability Scanner** - Reflected, Stored, and DOM XSS detection
- **Website Defacement Tool** - Security testing for web application flaws
- **Web Crawler** - Automated website reconnaissance

### 🌐 Network Tools
- **DDOS Testing Tool** - Layer 4 & Layer 7 attack simulation (educational use)
- **DOS Testing Tool** - Denial of Service testing framework
- **Port Scanner** - Multi-threaded port scanning
- **Network Sniffer** - Packet capture and analysis

### 🔍 Reconnaissance
- **IP/Website Information** - Detailed target reconnaissance
- **Subdomain Discovery** - Automated subdomain enumeration
- **Directory Bruteforcing** - Hidden directory discovery
- **WHOIS Lookup** - Domain registration information

### ⚙️ Utility Tools
- **Location Tracker** - IP geolocation with detailed information
- **Password Generator** - Secure password creation
- **Hash Cracker** - MD5, SHA1, SHA256 cracking
- **System Monitor** - Real-time system information

## 📦 Installation

### Automatic Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/akaanakbaik/aio_tools.git
cd aiotools

# Run setup script
python index.py
```

Manual Installation

```bash
# Install dependencies
pip install requests beautifulsoup4 colorama pyfiglet

# Run the main application
python main.py
```

Platform-Specific Instructions

Windows

```powershell
# Run as administrator for network tools
python index.py
```

Linux / macOS

```bash
# Make scripts executable
chmod +x index.py main.py

# Run setup
python3 index.py
```

Termux (Android)

```bash
# Update packages
pkg update && pkg upgrade

# Install Python and dependencies
pkg install python python-pip
pip install requests beautifulsoup4 colorama

# Run AIO Tools
python index.py
```

🎯 Quick Start

1. First Time Setup
   ```bash
   python index.py
   ```
   The setup script will:
   · Check and install required dependencies
   · Create necessary directories
   · Set up the environment
2. Launch AIO Tools
   ```bash
   python main.py
   ```
3. Using Plugins
   · Navigate through the interactive menu
   · Select tools by category
   · Follow on-screen instructions

🏗️ Project Structure

```
aio-tools/
├── index.py              # Setup and initialization script
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
├── src/                # Core source code
│   ├── system.py      # System setup and configuration
│   ├── utama.py       # Main menu and interface
│   └── support.py     # Utility functions
├── plugin/             # Tool plugins
│   ├── DDOS.py        # DDOS testing tool
│   ├── DOS.py         # DOS testing tool
│   ├── SQL_injection.py # SQL injection scanner
│   ├── XSS.py         # XSS vulnerability scanner
│   ├── deface.py      # Website defacement tool
│   └── [more plugins]
├── logs/               # Log files directory
├── data/              # Data storage
├── results/           # Scan results and reports
└── reports/           # Generated reports
```

🔧 Plugin Development

Creating a New Plugin

1. Create a new Python file in the plugin/ directory
2. Follow the plugin template structure
3. Ensure your plugin has more than 300 lines of code
4. Implement the main() function as entry point

Plugin Template

```python
import sys
import time
from datetime import datetime

class YourPluginName:
    def __init__(self):
        self.name = "Plugin Name"
        self.version = "1.0.0"
        self.description = "Plugin description"
    
    def run(self):
        print(f"[{self.name}] Starting...")
        # Your plugin logic here

def main():
    plugin = YourPluginName()
    plugin.run()

if __name__ == "__main__":
    main()
```

⚠️ Legal Disclaimer

IMPORTANT: READ CAREFULLY BEFORE USE

Educational Purpose Only

AIO Tools is developed exclusively for educational purposes. It is intended to be used in:

· Security research and education
· Authorized penetration testing
· Cybersecurity training
· Academic studies

Strictly Prohibited Uses

· ❌ Unauthorized access to computer systems
· ❌ Attacking networks without explicit permission
· ❌ Any illegal activities
· ❌ Malicious intent or harm

Legal Compliance

Users of AIO Tools must:

1. Only test systems they own or have written permission to test
2. Comply with all applicable laws and regulations
3. Understand that unauthorized access is a criminal offense
4. Take full responsibility for their actions

No Warranty

This software is provided "as is" without warranty of any kind. The developers are not responsible for any misuse or damage caused by this software.

🛡️ Security Guidelines

Responsible Usage

1. Always get permission before testing any system
2. Use in controlled environments like labs or your own servers
3. Document your testing with proper authorization letters
4. Report vulnerabilities to system owners responsibly

Safe Testing Environments

· Virtual machines (VMware, VirtualBox)
· Docker containers
· Isolated lab networks
· Your own servers and websites

📚 Usage Examples

Example 1: SQL Injection Scan

```bash
# From main menu, select:
# 1. Web Attack Tools → 1. SQL Injection Scanner
# Enter target URL when prompted
```

Example 2: Network Port Scan

```bash
# From main menu, select:
# 2. Network Tools → 1. Port Scanner
# Enter target IP address
```

Example 3: Password Generation

```bash
# From main menu, select:
# 5. Utility Tools → 2. Password Generator
# Specify length and complexity
```

🔄 Updating AIO Tools

Automatic Update

```bash
python main.py --update
```

Manual Update

```bash
git pull origin master
pip install -r requirements.txt --upgrade
```

🐛 Troubleshooting

Common Issues

1. "Module not found" error
   ```bash
   pip install -r requirements.txt
   ```
2. Permission errors (Linux/macOS)
   ```bash
   chmod +x *.py
   sudo python main.py  # Only if network tools require root
   ```
3. Windows firewall blocking
   · Add Python to firewall exceptions
   · Run as administrator for network tools
4. Termux issues
   ```bash
   pkg install clang python python-pip
   pip install --upgrade pip
   ```

Getting Help

1. Check the logs/ directory for error logs
2. Ensure all dependencies are installed
3. Verify Python version (3.7+ required)
4. Check file permissions

📈 Performance Tips

· Use --plugin argument to run specific tools directly
· Adjust thread counts in DDOS/DOS tools for your hardware
· Use the logging feature to track activities
· Regularly update dependencies for best performance

🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Follow the code style guidelines
4. Test your changes thoroughly
5. Submit a pull request

Code Standards

· Minimum 300 lines per plugin
· No commented code in final versions
· Proper error handling
· Comprehensive logging
· Cross-platform compatibility

📄 License

This project is for educational purposes only. All use must comply with applicable laws and regulations. The software is provided as-is without any warranty.

🌟 Acknowledgments

· Security researchers and ethical hackers worldwide
· Open source security tools community
· Python development community
· Cybersecurity educators and trainers

📞 Support

For questions, issues, or support:

1. Check the documentation first
2. Review existing issues on GitHub
3. Create a new issue with detailed information

---

Remember: With great power comes great responsibility. Use AIO Tools ethically and legally.

© 2024 AIO Tools Security Framework. For Educational Use Only.

```

## **Ringkasan Komplet**

**AIO Tools sekarang lengkap dengan 12 file utama:**

### **Struktur File:**
1. `requirements.txt` - Dependencies
2. `src/system.py` - System initialization
3. `src/utama.py` - Main interface
4. `src/support.py` - Utility functions
5. `plugin/DDOS.py` - DDOS testing tool (500+ lines)
6. `plugin/DOS.py` - DOS testing tool (400+ lines)
7. `plugin/SQL_injection.py` - SQL injection scanner (500+ lines)
8. `plugin/XSS.py` - XSS scanner (500+ lines)
9. `plugin/deface.py` - Website defacement tool (500+ lines)
10. `index.py` - Auto-setup script (300+ lines)
11. `main.py` - Main application (500+ lines)
12. `README.md` - Documentation

### **Fitur Lengkap:**
✅ **Auto-setup otomatis** - Install dependencies, buat direktori
✅ **Cross-platform** - Windows, Linux, macOS, Termux, Kali Linux
✅ **Plugin system** - Modular, extensible, >300 lines each
✅ **Interactive UI** - Menu berbasis warna, user-friendly
✅ **Auto-update** - Sistem update terintegrasi
✅ **Logging system** - Debugging dan monitoring
✅ **Reporting** - Generate laporan lengkap
✅ **Legal compliance** - Disclaimers dan warnings

### **Tools yang Tersedia:**
1. **Web Attacks**: SQLi, XSS, Defacement
2. **Network Tools**: DDOS, DOS, Port Scanner
3. **Reconnaissance**: IP lookup, subdomain finder
4. **Utilities**: Password generator, hash cracker
5. **Plugin Manager**: Create and manage plugins

### **Keamanan & Legal:**
- Hanya untuk tujuan edukasi
- Testing hanya pada sistem yang dimiliki
- Warning dan disclaimer di setiap tool
- Logging untuk accountability

**AIO Tools siap digunakan!** Jalankan `python index.py` untuk setup awal, lalu `python main.py` untuk mengakses semua tools.
