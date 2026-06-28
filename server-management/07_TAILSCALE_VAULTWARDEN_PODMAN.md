# 07: Tailscale + Vaultwarden + Podman on Low-RAM Hardware

A highly detailed engineering guide for deploying a containerized Vaultwarden instance on resource-constrained platforms (such as the Raspberry Pi Zero 2W with 512MB RAM) using Podman (daemonless) and Tailscale.

---

## 1. Operating System & Hardware Optimizations (DietPi/Debian Minimal)

On systems with only 512MB of RAM, every megabyte matters. Prior to container execution, the host OS must be stripped of unnecessary services and hardware allocations.

### A. GPU Memory Reallocation
The default Raspberry Pi firmware allocates precious system RAM to the GPU. On a headless server, this memory must be reclaimed.
1. Open the boot configuration file (typically `/boot/firmware/config.txt` or `/boot/config.txt` depending on OS version):
   ```bash
   sudo nano /boot/firmware/config.txt
   ```
2. Verify or append the following values at the end of the file:
   ```text
   gpu_mem=16
   ```
   *(16MB is the absolute minimum allowed by the hardware kernel, freeing up to 48MB of RAM for the system).*

### B. Pruning Redundant Daemons
Turn off high-overhead or unnecessary background services:
```bash
# Disable Bluetooth, system sounds, and Avahi Multicast DNS (replaced by Tailscale MagicDNS)
sudo systemctl disable --now bluetooth.service avahi-daemon.service avahi-daemon.socket triggerhappy.service
```

---

## 2. Podman Container Integration (Daemonless Migration)

While Docker is the industry standard, its resident background processes (`dockerd` and `containerd`) consume upwards of 50MB of RAM statically. **Podman** is a *daemonless* container engine that spawns containers directly as child processes of the invoking shell or systemd, eliminating background process overhead.

### A. Migrating from Docker to Podman without Data Loss
Since your database in `~/vw-data` resides on the host system filesystem, removing Docker containers will **never** delete your passwords. Podman can safely bind-mount the existing directory.

1. Install Podman and clean up Docker resources:
   ```bash
   sudo apt update && sudo apt install podman -y
   docker stop vaultwarden && docker rm vaultwarden
   sudo systemctl disable --now docker.service docker.socket
   ```
2. Spin up Vaultwarden under Podman using hyper-focused memory and runtime thread constraints:
   ```bash
   podman run -d --name vaultwarden \
     -e ROCKET_WORKERS=2 \
     -e DATABASE_MAX_CONNECTIONS=2 \
     -v /home/<YOUR_USERNAME>/vw-data:/data/ \
     -p 127.0.0.1:8080:80 \
     --restart always \
     docker.io/vaultwarden/server:latest
   ```
   * `--memory="50m"` limits the physical RAM allocation.
   * `ROCKET_WORKERS=2` prevents the Rocket web server from spawning 8 threads (default on 4-core Pi Zero 2W), restricting it to a lightweight footprint.
   * `DATABASE_MAX_CONNECTIONS=2` keeps the SQLite transaction pool compact.
   * `-p 127.0.0.1:8080:80` isolates Vaultwarden strictly on the local host loopback, denying access from external network interfaces.

### B. Creating Systemd Persistence
To ensure Podman containers start automatically upon system reboots without a running daemon:
```bash
podman generate systemd --new --name vaultwarden --files
sudo mv container-vaultwarden.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable container-vaultwarden.service
```

---

## 3. Resolving iOS 18.2 DNS & SSL Handshake Failures

Modern mobile platforms like iOS 18.2 enforce rigid security parameters. The Bitwarden/Vaultwarden application will **refuse to transmit passwords over unencrypted HTTP connections** (throwing `Subtle Crypto API` errors). Accessing via plain IP addresses (`http://<YOUR_TAILSCALE_IP>:8080`) is blocked. We must force an encrypted HTTPS channel.

### A. Why Tailscale MagicDNS and `.ts.net` May Fail
Under iOS 18.2, security mechanisms can bypass local VPN DNS configurations (such as Tailscale's MagicDNS server `100.100.100.100`), routing `.ts.net` queries through public DNS servers or Apple's iCloud Private Relay. When this happens, the domain name cannot be resolved, resulting in a "Cannot Open Page" timeout.

**Remediation Steps for iOS 18.2:**
1. **Deactivate iCloud Private Relay:** Go to **Settings** -> **[Your Name]** -> **iCloud** -> **Private Relay** -> Set to **Off**.
2. **Deactivate IP Tracking Restrictions:** Go to **Settings** -> **Wi-Fi** -> Tap the **(i)** icon next to your network -> Toggle off **Limit IP Address Tracking**.
3. **Override Local DNS in Tailscale:** Go to your [Tailscale Admin Console](https://login.tailscale.com/admin/dns) under **Settings -> DNS**. Locate the **Nameservers** panel and enable **Override local DNS**. This forces iOS to use MagicDNS.
4. **Local Network Permission Check:** On iOS, go to **Settings** -> **Tailscale** and verify **Local Network** is active.
