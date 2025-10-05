#!/usr/bin/env python3
"""
Application Health Checker
Pings an HTTP/HTTPS endpoint and decides UP/DOWN by status code.

Usage:
  python healthcheck.py --url https://example.com --retries 3 --timeout 5

Exit codes:
  0 - All checks passed (UP)
  2 - One or more checks failed (DOWN)
"""

import argparse
import sys
import time

try:
    import requests
except ImportError:
    raise SystemExit(
        "requests not installed. Install with: pip install -r requirements.txt"
    )

def parse_args():
    p = argparse.ArgumentParser(description="HTTP health checker")
    p.add_argument("--url", required=True, help="URL to check (http/https)")
    p.add_argument("--retries", type=int, default=3, help="Retry attempts (default: 3)")
    p.add_argument("--timeout", type=int, default=5, help="Seconds timeout per request")
    return p.parse_args()

def check(url, retries, timeout):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=timeout)
            code = r.status_code
            if 200 <= code < 400:
                print(f"[UP] {url} responded {code} on attempt {attempt}")
                return True
            else:
                print(f"[WARN] {url} responded {code} on attempt {attempt}")
        except requests.RequestException as e:
            print(f"[ERROR] Attempt {attempt} failed: {e}")
        time.sleep(1)
    return False

def main():
    args = parse_args()
    if check(args.url, args.retries, args.timeout):
        sys.exit(0)
    else:
        print(f"[DOWN] {args.url} is not healthy after {args.retries} attempts")
        sys.exit(2)

if __name__ == "__main__":
    main()
