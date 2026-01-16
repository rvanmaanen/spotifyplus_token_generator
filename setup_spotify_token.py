#!/usr/bin/env python3
"""
Spotify Token Setup Script
Downloads and runs the official AuthTokenGenerator.py, then serves the token file for download.
"""

import os
import sys
import subprocess
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

SCRIPT_URL = "https://raw.githubusercontent.com/thlucas1/SpotifyWebApiPython/master/docs/include/samplecode/ZeroconfConnect/AuthTokenGenerator.py"
SCRIPT_NAME = "AuthTokenGenerator.py"
TOKEN_FILE = "spotifyplus_tokens.json"

def download_script():
    """Download the official AuthTokenGenerator.py script"""
    print("Downloading AuthTokenGenerator.py...")
    try:
        urllib.request.urlretrieve(SCRIPT_URL, SCRIPT_NAME)
        print(f"✓ Downloaded {SCRIPT_NAME}")
        return True
    except Exception as e:
        print(f"✗ Failed to download script: {e}")
        return False

def run_generator():
    """Run the AuthTokenGenerator.py script"""
    print("\nRunning AuthTokenGenerator.py...")
    print("=" * 70)
    try:
        result = subprocess.run([sys.executable, SCRIPT_NAME], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except KeyboardInterrupt:
        print("\n\nScript cancelled by user")
        return False

def serve_file():
    """Start a simple HTTP server to serve the token file"""
    if not os.path.exists(TOKEN_FILE):
        print(f"\n✗ Token file '{TOKEN_FILE}' not found. Generation may have failed.")
        return
    
    print("\n" + "=" * 70)
    print("SUCCESS! Token file generated.")
    print("=" * 70)
    print("\nStarting download server...")
    
    class TokenFileHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == f'/{TOKEN_FILE}':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Content-Disposition', f'attachment; filename="{TOKEN_FILE}"')
                self.end_headers()
                with open(TOKEN_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = f"""
                <html>
                <head><title>Download Spotify Token</title></head>
                <body style="font-family: Arial, sans-serif; padding: 50px; text-align: center;">
                    <h1>🎵 Spotify Token Ready!</h1>
                    <p>Click the button below to download your token file:</p>
                    <p><a href="/{TOKEN_FILE}" download style="display: inline-block; padding: 15px 30px; background: #1DB954; color: white; text-decoration: none; border-radius: 5px; font-size: 18px;">Download {TOKEN_FILE}</a></p>
                    <hr style="margin: 30px 0;">
                    <p style="color: #666;">Copy this file to your Home Assistant server:</p>
                    <code style="background: #f0f0f0; padding: 10px; display: block;">/config/.storage/spotifyplus_tokens.json</code>
                    <p style="margin-top: 30px; color: #999;">Press Ctrl+C in the terminal to stop this server</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
        
        def log_message(self, format, *args):
            """Suppress request logging"""
            pass
    
    port = 8000
    server = HTTPServer(('0.0.0.0', port), TokenFileHandler)
    
    print(f"\n✓ Server running at:")
    print(f"   http://localhost:{port}/")
    print(f"\nDirect download link:")
    print(f"   http://localhost:{port}/{TOKEN_FILE}")
    print(f"\nPress Ctrl+C to stop the server")
    print("=" * 70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

if __name__ == "__main__":
    # Download the script
    if not download_script():
        sys.exit(1)
    
    # Run the generator
    if not run_generator():
        print("\n✗ Token generation failed or was cancelled.")
        sys.exit(1)
    
    # Serve the file for download
    serve_file()
