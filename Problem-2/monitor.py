#!/usr/bin/env python3
"""
System Health Monitoring Script
Checks CPU, Memory, Disk utilization and basic process info.
Logs to console and to system_health.log.
Thresholds can be passed via CLI or environment variables.

Usage examples:
  python monitor.py
  python monitor.py --cpu 85 --mem 85 --disk 90
Env vars (optional):
  CPU_THRESHOLD, MEM_THRESHOLD, DISK_THRESHOLD
"""

import argparse
import logging
import os
import platform
import time
from datetime import datetime

try:
    import psutil
except ImportError:
    raise SystemExit(
        "psutil not installed. Install with: pip install -r requirements.txt"
    )

LOG_FILE = os.path.join(os.path.dirname(__file__), "system_health.log")

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )

def parse_args():
    def env_int(name, default):
        try:
            return int(os.getenv(name, default))
        except ValueError:
            return default

    p = argparse.ArgumentParser(description="System Health Monitor")
    p.add_argument("--cpu", type=int, default=env_int("CPU_THRESHOLD", 80),
                   help="CPU usage threshold percent (default: 80)")
    p.add_argument("--mem", type=int, default=env_int("MEM_THRESHOLD", 80),
                   help="Memory usage threshold percent (default: 80)")
    p.add_argument("--disk", type=int, default=env_int("DISK_THRESHOLD", 80),
                   help="Disk usage threshold percent (default: 80)")
    p.add_argument("--interval", type=int, default=1,
                   help="Seconds to wait while sampling CPU (default: 1)")
    return p.parse_args()

def check_metrics(cpu_thr, mem_thr, disk_thr, interval):
    cpu = psutil.cpu_percent(interval=interval)
    mem = psutil.virtual_memory().percent
    # Root mount works on Linux. On Windows, C:\ works.
    disk_path = "/" if os.name != "nt" else "C:\\"
    disk = psutil.disk_usage(disk_path).percent

    proc_count = len(psutil.pids())

    status = "OK"
    if cpu > cpu_thr or mem > mem_thr or disk > disk_thr:
        status = "ALERT"

    msg = (f"Host={platform.node()} | CPU={cpu:.1f}% "
           f"MEM={mem:.1f}% DISK={disk:.1f}% procs={proc_count}")

    if status == "ALERT":
        logging.warning(msg + f" | Thresholds cpu/mem/disk={cpu_thr}/{mem_thr}/{disk_thr}")
    else:
        logging.info(msg + " | All metrics within thresholds")

    return status, {"cpu": cpu, "mem": mem, "disk": disk, "procs": proc_count}

def main():
    setup_logger()
    args = parse_args()

    start = datetime.utcnow()
    status, metrics = check_metrics(args.cpu, args.mem, args.disk, args.interval)
    end = datetime.utcnow()

    logging.info(
        f"Run complete | status={status} | started={start.isoformat()}Z | ended={end.isoformat()}Z"
    )

    # Exit code useful for schedulers/CI
    raise SystemExit(0 if status == "OK" else 2)

if __name__ == "__main__":
    main()
