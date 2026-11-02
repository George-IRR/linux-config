# 10: Homer Static Dashboard Configuration

Configuration and deployment of Homer, a dead-simple static dashboard served via Nginx with sub-10MB RAM footprint, configured entirely via declarative YAML files.

---

## 1. Directory Structure & Permissions

Prepare the assets mount point for custom YAML definitions and icon sets:

```bash
sudo mkdir -p /opt/stacks/homer/assets
sudo chown -R $USER:$USER /opt/stacks/homer
```

---

## 2. Compose Definition & Asset Initialization

Deploy the containerized service inside `/opt/stacks/homer/compose.yaml`:

```yaml
services:
  homer:
    image: b4bz/homer:latest
    container_name: homer
    restart: unless-stopped
    ports:
      - "8010:8080"
    volumes:
      - /opt/stacks/homer/assets:/www/assets
    environment:
      - UID=1000
      - GID=1000
```

Start the stack:
```bash
cd /opt/stacks/homer
docker compose up -d
```

Inject hardened, clean production configuration into `/opt/stacks/homer/assets/config.yml`:

```bash
cat << 'EOF' > /opt/stacks/homer/assets/config.yml
---
title: "Home Infrastructure"
subtitle: "Node Operations Dashboard"
logo: "logo.png"

header: true
footer: false
theme: default
message: false
columns: "3"

links:
  - name: "Tailnet Console"
    icon: "fas fa-shield-alt"
    url: "https://login.tailscale.com/admin/machines"
    target: "_blank"

services:
  - name: "Core Management"
    icon: "fas fa-server"
    items:
      - name: "Dockge"
        icon: "fa-brands fa-docker"
        subtitle: "Stack Orchestration"
        tag: "stacks"
        url: "https://<hostname>.<tailnet>.ts.net:8443"
        target: "_blank"

  - name: "Services & Sync"
    icon: "fas fa-cubes"
    items:
      - name: "Linkding"
        icon: "fas fa-bookmark"
        subtitle: "Bookmark Archive"
        tag: "archive"
        url: "https://<hostname>.<tailnet>.ts.net:8444"
        target: "_blank"
EOF
```

---

## 3. Diagnostics & Validation

Verify container responsiveness and HTTP header response code:

```bash
curl -I http://localhost:8010/
```

### Expected Output
```text
HTTP/1.1 200 OK
Server: nginx
Content-Type: text/html
Content-Length: 1042
Connection: keep-alive
```

Verify real-time memory footprint:
```bash
docker stats --no-stream homer --format "table {{.Name}}	{{.MemUsage}}"
```

### Expected Output
```text
NAME      MEM USAGE / LIMIT
homer     6.21MiB / 3.65GiB
```

---

## 4. Best Practices (Do's and Don'ts)

* **DO:**
  * Keep `message: false` to disable placeholder demo banners in production.
  * Use relative local asset paths or trusted CDN URLs for icon assets.
  * Leverage `target: "_blank"` on external service links to prevent breaking dashboard state.

* **DON'T:**
  * Do NOT append URL hashes (`#`) to upstream target endpoints.
  * Do NOT leave default write permissions (`777`) on the `/www/assets` directory.
  * Do NOT run complex Node-based dashboards on hardware where every 100MB of RAM is critical.
