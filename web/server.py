#!/usr/bin/env python3
"""Serve the Helix web app and proxy Alpaca market-data requests.

The browser calls /api/alpaca/<path>; this server forwards the request to
https://data.alpaca.markets/<path> with the API keys attached, so the keys
never reach the page. Only read-only market-data paths are forwarded.

Keys come from ALPACA_API_KEY / ALPACA_SECRET_KEY, either in the environment
or in a .env file in this folder or the repository root.

    python3 web/server.py            # http://127.0.0.1:8000
    PORT=9000 python3 web/server.py
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALPACA_DATA = "https://data.alpaca.markets"
ALLOWED_PREFIXES = ("v2/stocks/", "v1beta3/crypto/")


def load_dotenv():
    for path in (HERE / ".env", HERE.parent / ".env"):
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


load_dotenv()
API_KEY = os.environ.get("ALPACA_API_KEY", "")
SECRET_KEY = os.environ.get("ALPACA_SECRET_KEY", "")
# Free Alpaca plans get IEX stock data; set ALPACA_DATA_FEED=sip with a paid plan.
FEED = os.environ.get("ALPACA_DATA_FEED", "iex")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        if url.path == "/api/config":
            return self.send_json(200, {"alpaca": bool(API_KEY and SECRET_KEY), "feed": FEED})
        if url.path.startswith("/api/alpaca/"):
            return self.proxy(url.path[len("/api/alpaca/"):], url.query)
        if url.path in ("/server.py", "/.env"):
            return self.send_error(404)
        return super().do_GET()

    def proxy(self, path, query):
        if not path.startswith(ALLOWED_PREFIXES) or ".." in path:
            return self.send_json(403, {"message": "path not allowed"})
        params = urllib.parse.parse_qs(query)
        if path.startswith("v2/stocks/") and "feed" not in params:
            query = (query + "&" if query else "") + "feed=" + FEED
        req = urllib.request.Request(f"{ALPACA_DATA}/{path}?{query}")
        if API_KEY and SECRET_KEY:
            req.add_header("APCA-API-KEY-ID", API_KEY)
            req.add_header("APCA-API-SECRET-KEY", SECRET_KEY)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status, body = resp.status, resp.read()
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read()
        except (urllib.error.URLError, TimeoutError) as e:
            return self.send_json(502, {"message": f"Alpaca unreachable: {e}"})
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if "/api/alpaca/" not in self.path:  # snapshots poll every few seconds
            super().log_message(fmt, *args)


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8000))
    if not (API_KEY and SECRET_KEY):
        print("ALPACA_API_KEY / ALPACA_SECRET_KEY not set: only crypto charts will load from Alpaca.")
    print(f"Helix running at http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
