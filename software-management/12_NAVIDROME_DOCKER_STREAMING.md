# 12: Navidrome Music Streaming Server Deployment via Docker Compose

Deployment guide for the lightweight Navidrome personal audio streaming server using Docker Compose, decoupling application state onto local SSD storage while reading music libraries from encrypted secondary USB storage, and configuring Tailscale Serve for remote HTTPS access without exposing ports to the public internet.

---

## 1. Directory Structure and Library Preparation

Organize persistent state volumes on high-speed internal SSD storage and maintain static music libraries on secondary storage.

1. Create application directories:
   ```bash
   mkdir -p ~/navidrome/data
   mkdir -p /mnt/usbstick_storage/music
   ```
2. Verify user and group ownership for rootless container execution:
   ```bash
   id -u $USER
   id -g $USER
   ```
   *(Standard UID/GID on Debian is `1000:1000`).*

---

## 2. Docker Compose Specification

Deploy Navidrome with the SQLite database mounted on internal storage for maximum query performance and the music folder mounted strictly as read-only.

Create `~/navidrome/docker-compose.yml`:

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    user: 1000:1000
    ports:
      - "4533:4533"
    restart: unless-stopped
    environment:
      ND_SCANSCHEDULE: "1h"
      ND_LOGLEVEL: "info"
      ND_SESSIONTIMEOUT: "24h"
      ND_BASEURL: ""
    volumes:
      - ./data:/data
      - /mnt/usbstick_storage/music:/music:ro
```

Launch the service:
```bash
cd ~/navidrome
docker compose up -d
```

---

## 3. Remote Access via Tailscale Serve HTTPS

Securely expose Navidrome to your private tailnet with automatic Let's Encrypt TLS certificates, eliminating the need for dynamic DNS or router port-forwarding:

```bash
# Expose Navidrome web UI on custom HTTPS port 8453 over Tailscale
sudo tailscale serve --bg --https=8453 4533
```

Verify active Serve status:
```bash
tailscale serve status
```

---

## 4. Diagnostics & Validation

### Validate Container Health & Port Listener
```bash
docker ps --filter name=navidrome --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

#### Expected Output
```text
NAMES       STATUS         PORTS
navidrome   Up 2 minutes   0.0.0.0:4533->4533/tcp, [::]:4533->4533/tcp
```

### Validate Web Endpoint
```bash
curl -I http://localhost:4533/app/
```

#### Expected Output
```text
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
...
```

---

## 5. Best Practices (Do's and Don'ts)

### Do's
- Always mount the media directory with the `:ro` (read-only) attribute in Docker to guarantee that containers cannot modify, corrupt, or delete original audio files.
- Keep `./data` on fast SSD storage so album art caching and database indexing remain responsive.
- Access the web UI initially at `http://<server-ip>:4533` to initialize the primary administrator account before exposing to other devices.

### Don'ts
- Do not place Navidrome's SQLite database directly on consumer USB flash drives, as constant write transactions will accelerate drive wear and degrade UI responsiveness.
- Do not expose port 4533 directly to the public internet without reverse proxy authentication or VPN protection.
