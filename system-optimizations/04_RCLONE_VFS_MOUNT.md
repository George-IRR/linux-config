# 04: Rclone VFS Mount Configuration

This configuration mounts a remote cloud drive as a local file system using `rclone` and `systemd`. It utilizes a Virtual File System (VFS) cache strategy optimized for fast browsing (metadata retention) while minimizing local disk footprint.

## Dependencies

Ensure the FUSE filesystem library and rclone are installed:

```bash
sudo apt update && sudo apt install rclone fuse3 -y
```

## Implementation: Systemd Service

First, create a dedicated mount directory for the user:
```bash
mkdir -p ~/Cloud/RemoteDrive
```

Next, create the systemd service file to handle automated background mounting.
**Path**: `/etc/systemd/system/rclone-mount.service`

```ini
[Unit]
Description=Rclone VFS Mount
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/rclone mount RemoteName: /home/USERNAME/Cloud/RemoteDrive \
  --config /home/USERNAME/.config/rclone/rclone.conf \
  --vfs-cache-mode full \
  --vfs-cache-max-age 10m \
  --vfs-cache-max-size 2G \
  --dir-cache-time 1000h \
  --poll-interval 1m \
  --buffer-size 32M \
  --vfs-read-chunk-size 32M
ExecStop=/bin/fusermount -u /home/USERNAME/Cloud/RemoteDrive
Restart=always
User=USERNAME
Group=USERNAME

[Install]
WantedBy=default.target
```

*(Note: Before applying, replace `RemoteName` with your configured rclone remote name, and replace `USERNAME` with your local Linux user).*

## Operations

1.  **Initialize**: Load the new service file into systemd.
    ```bash
    sudo systemctl daemon-reload
    ```
2.  **Enable**: Set the mount to trigger automatically on system boot.
    ```bash
    sudo systemctl enable rclone-mount.service
    ```
3.  **Execute**: Start the mount immediately.
    ```bash
    sudo systemctl start rclone-mount.service
    ```
4.  **Verify**: Check the operational status or view logs in case of failure.
    ```bash
    systemctl status rclone-mount.service
    journalctl -u rclone-mount.service -n 20
    ```

## Configuration Parameters Explained

The applied parameters are specifically tuned for a "Metadata-Heavy, File-Light" approach. This prioritizes instant directory browsing while aggressively clearing downloaded file contents to conserve local SSD space.

* **`--vfs-cache-mode full`**: Caches reads and writes to the local disk. This acts as a necessary buffer, preventing native Linux file managers (like Nautilus) from hanging or crashing when attempting to generate thumbnails or read file headers.
* **`--dir-cache-time 1000h`**: Retains the directory structure (metadata, filenames, timestamps) in memory for an extended period (~41 days). This allows near-instant folder navigation without requiring constant API calls to the cloud provider.
* **`--poll-interval 1m`**: Counterbalances the long directory cache. Rclone checks the remote server every minute for new changes (e.g., files modified via a phone or web browser) and invalidates stale local cache entries seamlessly.
* **`--vfs-cache-max-age 10m`**: Evicts actual file contents from the local cache 10 minutes after a file is closed. This ensures large files do not persist on the local drive after use.
* **`--vfs-cache-max-size 2G`**: Establishes a strict 2GB ceiling for local cache utilization. This provides just enough overhead for temporary documents and image thumbnails without bloating the local filesystem.
* **`--buffer-size 32M` & `--vfs-read-chunk-size 32M`**: Optimizes memory buffering and standardizes download chunks, preventing API throttling and ensuring smoother streaming of large files directly from the cloud.
