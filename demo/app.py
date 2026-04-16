"""
vibeguardian demo app

Demonstrates three vibeguardian features:

  1. Inject Mode  — MY_API_KEY is read from the environment, injected by `vg`
                    at runtime (never written to disk or .env).

  2. Log Mask     — The raw key is printed below, but `vg run` intercepts the
                    output and replaces it with ***[MASKED]*** before it reaches
                    your terminal.

  3. Proxy Mode   — An HTTP request is sent to localhost:8081/proxy/echo.
                    `vg` forwards it to the local echo server (port 9000) and
                    injects X-Api-Key automatically — the Python code never sees the key.

Run with:
    bash setup.sh
"""

import os
import sys

try:
    import urllib.request
    import json
except ImportError:
    pass  # stdlib only — no pip install needed


# ── 1. Inject Mode demo ──────────────────────────────────────────────────────

api_key = os.environ.get("MY_API_KEY", "")
app_env = os.environ.get("APP_ENV", "(not set)")

print("=" * 60)
print("vibeguardian demo")
print("=" * 60)
print()
print("[Inject Mode]")
print(f"  APP_ENV   = {app_env}")

if api_key:
    # This line intentionally prints the raw key.
    # vibeguardian's log masking will replace it with ***[MASKED]*** in the terminal.
    print(f"  MY_API_KEY = {api_key}  <-- should appear as ***[MASKED]***")
else:
    print("  MY_API_KEY = (not injected — are you running via `vg run`?)")
    sys.exit(1)

print()


# ── 2. Proxy Mode demo ───────────────────────────────────────────────────────

print("[Proxy Mode]")
proxy_url = "http://localhost:8081/proxy/echo/get?demo=vibeguardian"
print(f"  Sending GET {proxy_url}")
print("  (vg injects X-Api-Key header — Python never sees the key)")
print()

try:
    req = urllib.request.Request(proxy_url)
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = json.loads(resp.read())
        received_header = body.get("headers", {}).get("x-api-key", "(not found)")
        print(f"  Response headers seen by upstream: {json.dumps(body.get('headers', {}), indent=4)}")
        if received_header and received_header != "(not found)":
            print()
            print("  X-Api-Key was injected by the proxy.")
        else:
            print("  X-Api-Key header was NOT found — proxy may not be running.")
except OSError as e:
    print(f"  Could not reach proxy: {e}")
    print("  Make sure you ran: vs run -- python app.py  (proxy starts automatically)")

print()
print("=" * 60)
print("Demo complete.")
print("=" * 60)
