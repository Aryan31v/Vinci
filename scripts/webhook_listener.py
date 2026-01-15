#!/usr/bin/env python3
"""
🌍 Webhook Listener (Mobile Extension)
--------------------------------------
A simple HTTP server to receive data and append it to the Input Stream.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

INPUT_STREAM_PATH = "/storage/emulated/0/Download/Vinci/1 - 🧠 The Construct/2 - 🧩 Input Stream.md"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        with open(INPUT_STREAM_PATH, 'a', encoding='utf-8') as f:
            f.write(f"\n- [ ] 🌍 **Webhook Input:** {post_data}\n")
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data received and logged to Input Stream.")

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"📡 Webhook Listener active on port {port}...")
    print("Use: curl -X POST -d 'Your message' http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

