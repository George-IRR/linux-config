# 05: Systemd Service Management

Systemd is the initialization system and service manager for Ubuntu. It is responsible for starting and managing background services, including custom optimizations like compressed swap (`zramswap`) and cloud mounts (`rclone-mount.service`).

This document outlines the essential `systemctl` commands required to maintain these services.

## Service Control Commands

### Restarting a Service
If a service crashes or needs to be refreshed manually, use the `restart` command.
```bash
sudo systemctl restart <service-name>
```
*Example: `sudo systemctl restart zramswap`*

### Reloading Configurations (Critical Step)
If you manually edit a `.service` file (e.g., modifying the cache parameters of a mount), systemd will not recognize the changes immediately. You must reload the daemon before restarting the service:
```bash
sudo systemctl daemon-reload
sudo systemctl restart <service-name>
```

## Monitoring and Listing Services

### View Active Services
To view a clean list of all services currently running on the system:
```bash
systemctl list-units --type=service --state=running
```
*(Press `q` to exit the list view).*

### View All Installed Services
To see every service registered on the system, regardless of whether it is currently running, disabled, or failed:
```bash
systemctl list-unit-files --type=service
```
* Note: A state of `enabled` means the service will start automatically on boot. A state of `disabled` means it must be started manually.

### Search for a Specific Service
To filter the list of services for a specific keyword (useful for finding custom configurations), pipe the output into `grep`:
```bash
systemctl list-units --type=service | grep rclone
```

## Troubleshooting and Diagnostics

### Check for Failed Services
If system performance degrades or a custom automation fails to load, check for crashed services:
```bash
systemctl --failed --type=service
```

### Viewing Service Status and File Locations
To diagnose a specific service or find exactly where its configuration file is stored, use the `status` command:
```bash
systemctl status <service-name>
```
The output will display the current operational state, recent log entries, and the exact path to the `.service` file being loaded (indicated by the `Loaded:` line).

## File Architecture

Systemd looks for service files in specific directories based on how they were created:

1.  **Custom / User-Defined Services:**
    Services created manually (e.g., custom hardware scripts, cloud mounts) should be placed in:
    `/etc/systemd/system/`
2.  **Package-Installed Services:**
    Services installed automatically via package managers (e.g., `apt`) are typically located in:
    `/lib/systemd/system/` or `/usr/lib/systemd/system/`
