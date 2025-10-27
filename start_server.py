#!/usr/bin/env python3
"""
Simple HTTP server to test the leaderboard locally
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Start the HTTP server"""
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Server starting on http://localhost:{PORT}")
            print(f"📁 Serving files from: {script_dir}")
            print("\n📋 Available pages:")
            print(f"   • Main app: http://localhost:{PORT}/index.html")
            print(f"   • Test page: http://localhost:{PORT}/test_leaderboard.html")
            print("\n🔧 Debug tips:")
            print("   • Open browser developer tools (F12)")
            print("   • Check the Console tab for debug messages")
            print("   • Check the Network tab for data loading")
            print("\n⏹️  Press Ctrl+C to stop the server")
            print("-" * 50)
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/index.html')
            except:
                pass
                
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Please try a different port or stop the existing server.")
            print("   You can also try: python start_server.py --port 8001")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check for port argument
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            PORT = int(sys.argv[2])
        except (IndexError, ValueError):
            print("❌ Invalid port number. Using default port 8000")
    
    start_server()
