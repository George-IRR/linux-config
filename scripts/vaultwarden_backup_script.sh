#!/bin/bash

# ==============================================================================
# Script: vaultwarden_backup.sh
# Target OS: DietPi / Debian Minimal / Raspberry Pi OS
# Architecture: Zero local storage write operations / Stream directly to cloud
# Execution: Configure in 'crontab -e' or run manually as root
# ==============================================================================

# Configurations
TIMESTAMP_FILE="/home/<YOUR_USERNAME>/.vw_last_run"
RCLONE_CONFIG_NAME="<YOUR_RCLONE_REMOTE_NAME>"
RCLONE_CONFIG_PATH="/home/<YOUR_USERNAME>/.config/rclone/rclone.conf"
REMOTE_DESTINATION="<YOUR_REMOTE_CLOUD_PATH>"

NOW=$(date +%s)
WEEK_IN_SECONDS=604800  # Exactly 7 days

# 1. Time-gate verification (only execute if 7 days have elapsed since last run)
if [ -f "$TIMESTAMP_FILE" ]; then
    LAST_RUN=$(cat "$TIMESTAMP_FILE")
    INTERVAL=$((NOW - LAST_RUN))
    if [ "$INTERVAL" -lt "$WEEK_IN_SECONDS" ]; then
        # Silent exit to keep syslog and cron logs clean
        exit 0
    fi
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="vaultwarden_direct_$TIMESTAMP.tar.xz"

# 2. Check if Podman and container are active
if ! podman ps | grep -q "vaultwarden"; then
    echo "[!] Error: Vaultwarden container is not active or Podman is not running."
    exit 1
fi

# 3. Freeze Vaultwarden database memory operations to prevent transaction corruption
podman pause vaultwarden

# 4. Stream archiving process straight to rclone remote target
# PIPESTATUS is used to catch the exit status of rclone, not the tar command.
# XZ compression is restricted to level -3 to limit RAM allocation under low-memory configurations.
XZ_OPT="-3" tar -cJf - -C /home/<YOUR_USERNAME> vw-data | rclone --config "$RCLONE_CONFIG_PATH" rcat "$RCLONE_CONFIG_NAME:$REMOTE_DESTINATION/$ARCHIVE_NAME"
UPLOAD_STATUS=${PIPESTATUS[1]}

# 5. Instantly resume Vaultwarden database execution
podman unpause vaultwarden

# 6. If upload was successful, save the timestamp
if [ "$UPLOAD_STATUS" -eq 0 ]; then
    echo "$NOW" > "$TIMESTAMP_FILE"
    echo "[+] Backup successfully completed and uploaded to cloud: $ARCHIVE_NAME"
else
    echo "[!] Error: Rclone upload failed with status code $UPLOAD_STATUS"
    exit 1
fi