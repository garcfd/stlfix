#!/usr/bin/env python3
"""HTTP server that serves static files + /api/files listing STL files by size."""
import http.server
import json
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/files':
            stls = []
            for f in os.listdir(DIR):
                if f.lower().endswith('.stl'):
                    fp = os.path.join(DIR, f)
                    stls.append({'name': f, 'size': os.path.getsize(fp)})
            stls.sort(key=lambda x: x['size'], reverse=True)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(stls).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    os.chdir(DIR)
    srv = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'Serving {DIR} on http://localhost:{PORT}')
    srv.serve_forever()
