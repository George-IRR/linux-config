# 04: Rclone Multi-Protocol Storage Servers

Technical guide for replacing unstable synchronous aggregators (e.g., Alist softlock) with isolated asynchronous servers (WebUI, WebDAV, SFTP) running directly through the Rclone core.

---

## 1. Emergency Unlocking of Synchronous Databases (Alist Purge)
Synchronous applications lock the graphical user interface (UI) when external storage (FTP/WebDAV/Cloud) experiences high network latency. To unlock without web interface access:

```bash
# 1. Stop the locked process
sudo /opt/alist/alist stop

# 2. Manually remove the faulty mount from the SQLite database
sqlite3 /opt/alist/data/alist.db "DELETE FROM x_storages WHERE mount_path='/mount_name';"

# 3. Restart the service
sudo /opt/alist/alist start
```

## 2. Native Rclone WebUI Server
Displays a modern graphical interface based directly on verified profiles in rclone.conf, completely eliminating intermediaries:

```bash
rclone rcd --rc-web-gui --rc-addr :5555 --rc-user george --rc-pass ACCESS_PASSWORD
```

## 3. Isolated SFTP Server (Bypassing Authentication Errors)
When exposing storage (e.g., mega_private:) via the SFTP protocol, clients (e.g., FileZilla) might automatically send the system's global public SSH keys (~/.ssh/id_rsa), causing the error:
`SSH login failed: [..., too many authentication failures]`

### Foreground Launch with Security Filtering
Forces Rclone to ignore the host's SSH infrastructure and accept exclusively the defined plain-text password:

```bash
rclone serve sftp mega_private: --addr :2222 --user admin --pass password --authorized-keys /dev/null
```

### Automation via Persistent Background Option (systemd)
Since the `serve sftp` subcommand does not accept the native `--daemon` flag, persistence is configured as a system service.
Path: `/etc/systemd/system/rclone-sftp.service`

```ini
[Unit]
Description=Rclone SFTP Server Background Engine
After=network.target

[Service]
Type=simple
User=george
ExecStart=/usr/bin/rclone serve sftp mega_private: --addr :2222 --user admin --pass password --authorized-keys /dev/null
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 4. Multi-Cloud Aggregation via FTP/SFTP (Combined Architecture)
To expose all configured clouds in separate directories within the same secure connection:
Add the `combine` type to the end of the `/home/george/.config/rclone/rclone.conf` file:

```ini
[all_clouds]
type = combine
upstreams = gdrive=GoogleDriveMain190: onedrive=Onedrive: mega=mega_private:
```

Execute the mapped server on the unified structure:

```bash
nohup rclone serve sftp all_clouds: --addr :2222 --user admin --pass password --authorized-keys /dev/null > /dev/null 2>&1 &
```

## 5. Tips & Backend Limits (Mega.nz)
* **2FA Lockout:** If you have enabled two-factor authentication (2FA) on your Mega account, the go-mega library used by Rclone will reject the connection directly at the handshake. 2FA must be disabled for dedicated CLI access.
* **RAM Consumption:** End-to-end encryption in Mega forces Rclone to download and decrypt the entire directory node into RAM during initialization. The process might seem frozen for a few minutes on large accounts.
* **Quick stop background server:** `pkill -f "rclone serve sftp"`
