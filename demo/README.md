# vibesafer demo

Demonstrates three core vibesafer features — Inject, Log Mask, and Proxy — with no external services and no pip dependencies.

## Files

```
demo/
  vibesafe.toml   # Project config (safe to commit — no real secrets inside)
  app.py          # Demo application
  echo_server.py  # Local HTTP server that acts as the proxy target
  setup.sh        # One-shot setup and run script
```

## Requirements

- `vs` installed (`vs --version` to verify)
- Python 3 available (`python3 --version` to verify)

## Usage

```bash
cd demo/
bash setup.sh
```

## What setup.sh does

### [1/3] Register a fake secret

```bash
vs set global/demo/api_key "sk_demo_1234567890abcdef"
```

Saves a fake API key to `~/.vibesafe/secrets.json`.  
The `secret://global/demo/api_key` reference in `vibesafe.toml` resolves to this value at runtime.  
In a real project, you would store your actual API key here instead.

### [2/3] Start the local echo server

```bash
python3 echo_server.py &   # background, port 9000
```

A minimal HTTP server that returns the incoming request's URL, method, and headers as JSON.  
This lets the demo verify that `vs` injected the `X-Api-Key` header without relying on any external service.  
The server is automatically stopped when `setup.sh` exits.

### [3/3] Run the demo app under vibesafer

```bash
vs run -- python3 app.py
```

`vs run` simultaneously:

1. Reads `~/.vibesafe/secrets.json`, resolves `MY_API_KEY` and `APP_ENV`, and injects them into `app.py`'s environment — no `.env` file written to disk.
2. Starts a local reverse proxy on port 8081 that forwards `/proxy/echo/*` to `localhost:9000` and injects `X-Api-Key` into every request.
3. Intercepts `app.py`'s stdout/stderr and replaces any secret value with `***[MASKED]***` before printing to your terminal.

## Expected output

```
[Vibesafe] Proxy started at http://localhost:8081
[Vibesafe] Injected 2 env var(s) (profile: dev)
[Vibesafe] Log masking enabled

============================================================
vibesafer demo
============================================================

[Inject Mode]
  APP_ENV    = ***[MASKED]***
  MY_API_KEY = ***[MASKED]***  <-- should appear as ***[MASKED]***

[Proxy Mode]
  Sending GET http://localhost:8081/proxy/echo/get?demo=vibesafer
  (vs injects X-Api-Key header — Python never sees the key)

  Response headers seen by upstream: {
    "x-api-key": "***[MASKED]***",
    ...
  }

  X-Api-Key was injected by the proxy.

============================================================
Demo complete.
============================================================
```

## What to look for

| Feature | What to verify |
|---|---|
| **Inject Mode** | `MY_API_KEY` is available as an env var — no `.env` file needed |
| **Log Mask** | The raw key value never appears in the terminal; only `***[MASKED]***` |
| **Proxy Mode** | `app.py` only talks to `localhost:8081`; the echo server response contains `x-api-key` injected by `vs` |

## Data flow

```
app.py
  │  GET http://localhost:8081/proxy/echo/get
  ▼
vs proxy (port 8081)
  │  injects X-Api-Key header
  │  GET http://localhost:9000/get
  ▼
echo_server.py (port 9000)
  │  returns request URL + headers as JSON
  ▼
vs proxy → app.py prints the response
  │  any secret value in stdout is replaced with ***[MASKED]***
  ▼
terminal
```
