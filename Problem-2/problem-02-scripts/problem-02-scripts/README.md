# Problem 2 – Scripts

This folder contains two scripts that satisfy the assignment:

1. **System Health Monitoring Script** – `monitor.py`  
   - Checks CPU, memory, disk utilization and process count.  
   - Thresholds default to 80% and can be passed via CLI or env vars:  
     `CPU_THRESHOLD`, `MEM_THRESHOLD`, `DISK_THRESHOLD`.  
   - Logs to console + `system_health.log` in this folder.  
   - **Run:**  
     ```bash
     pip install -r requirements.txt
     python monitor.py --cpu 85 --mem 85 --disk 90
     ```
   - **Schedule (cron example):**  
     `*/5 * * * * /usr/bin/python3 /path/to/problem-02-scripts/monitor.py >> /var/log/monitor.cron.log 2>&1`

2. **Application Health Checker** – `healthcheck.py`  
   - Verifies an application by HTTP status code (2xx/3xx = UP).  
   - Retries and timeout are configurable.  
   - Exit code `0` for UP, `2` for DOWN.  
   - **Run:**  
     ```bash
     pip install -r requirements.txt
     python healthcheck.py --url https://example.com --retries 3 --timeout 5
     ```
