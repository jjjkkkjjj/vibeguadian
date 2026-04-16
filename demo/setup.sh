#!/usr/bin/env bash
# setup.sh — one-time setup for the vibeguardian demo
#
# 1. Stores a fake API key in ~/.vibeguard/secrets.json
# 2. Starts a local echo server (port 9000) in the background
# 3. Runs the demo app via `vg run`
#
# Usage:
#   cd demo/
#   bash setup.sh

set -euo pipefail

cd "$(dirname "$0")"

FAKE_KEY="sk_demo_1234567890abcdef"

echo "========================================"
echo " vibeguardian demo setup"
echo "========================================"
echo ""
echo "[1/3] Storing fake API key in ~/.vibeguard/secrets.json ..."
echo "      path : global/demo/api_key"
echo "      value: ${FAKE_KEY}"
echo ""

vg set global/demo/api_key "${FAKE_KEY}"

echo ""
echo "[2/3] Starting local echo server on http://localhost:9000 ..."

python3 echo_server.py &
ECHO_PID=$!
trap "kill ${ECHO_PID} 2>/dev/null; echo ''; echo '[echo-server] stopped.'" EXIT

# Wait until the echo server is ready
for i in $(seq 1 10); do
    if python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:9000', timeout=1)" 2>/dev/null; then
        break
    fi
    sleep 0.3
done

echo ""
echo "[3/3] Running demo app via 'vg run' ..."
echo "      Watch for ***[MASKED]*** in the output below."
echo ""

vg run -- python3 app.py
