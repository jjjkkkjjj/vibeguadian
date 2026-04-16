#!/usr/bin/env python3
"""
Local echo server for the vibesafer proxy demo.

Returns the incoming request's URL, method, and headers as JSON.
This lets the demo verify that vs injected X-Api-Key without relying
on any external service.

Port: 9000
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 9000


class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(
            {
                "url": self.path,
                "method": "GET",
                "headers": dict(self.headers),
            },
            indent=2,
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # suppress default access log
        print(f"[echo-server] {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), EchoHandler)
    print(f"[echo-server] Listening on http://localhost:{PORT}", flush=True)
    server.serve_forever()
