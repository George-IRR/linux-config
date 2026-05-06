# 16: Automated Backup Scheduling

Documentation for automating the `zpaqfranz` backup process using `systemd` services and timers. This ensures container data is archived on a strict schedule without manual intervention, while funneling all output to the system journal for easy troubleshooting.

## 1. The Execution Script
Create a dedicated shell script that safely stops the container, runs the backup, and restarts the container.

**Path:** `/usr/local/bin/run-app-backup.sh`
```bash
#!/bin/bash
# Stop the container to ensure database consistency
docker stop app_container_name

# Execute the hardened multipart backup
zpaqfranz backup "/mnt/backups/app_data_???????.zpaq" /opt/containers/app_data/ \
  -index "/mnt/backups/index_maps/" -m2 -tar -checksize 10g \
  -key "SuperSecretPassword" -tmp -test -backupxxh3 -filelist -not "*/cache/*"

# Restart the container
docker start app_container_name
```
*(Make the script executable: `sudo chmod +x /usr/local/bin/run-app-backup.sh`)*

## 2. The Systemd Service
Create the service unit that tells `systemd` how to execute the script.

**Path:** `/etc/systemd/system/app-backup.service`
```ini
[Unit]
Description=Execute Hardened Application Backup
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/run-app-backup.sh
User=root
```

## 3. The Systemd Timer
Create the timer unit that dictates *when* the service runs (e.g., daily at 3:00 AM).

**Path:** `/etc/systemd/system/app-backup.timer`
```ini
[Unit]
Description=Daily Application Backup Timer

[Timer]
# Run every day at 3:00 AM
OnCalendar=*-*-* 03:00:00
# If the system was off at 3 AM, run it immediately upon booting
Persistent=true

[Install]
WantedBy=timers.target
```

## Operations
1. **Initialize daemon:** `sudo systemctl daemon-reload`
2. **Enable timer:** `sudo systemctl enable app-backup.timer`
3. **Start timer:** `sudo systemctl start app-backup.timer`
4. **Verify schedule:** `systemctl list-timers | grep app-backup`
5. **Check execution logs:** `journalctl -u app-backup.service`
