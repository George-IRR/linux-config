# 09: Dockge Lightweight Compose Management

Deployment and configuration of Dockge, an ultra-low footprint (~20MB RAM) Docker Compose manager designed for resource-constrained hosts with standard directory structures and non-root group execution.

---

## 1. Directory Scaffolding & Environment Setup

Establish standardized directories for Dockge runtime and persistent stack configurations:

```bash
# Create dedicated directories
sudo mkdir -p /opt/dockge /opt/stacks

# Grant administrative ownership to non-root operator
sudo chown -R $USER:$USER /opt/dockge /opt/stacks
```

---

## 2. Stack Deployment Configuration

Create the compose configuration file in `/opt/dockge/compose.yaml`:

```yaml
services:
  dockge:
    image: louislam/dockge:1
    container_name: dockge
    restart: unless-stopped
    ports:
      - "5001:5001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /opt/dockge/data:/app/data
      - /opt/stacks:/opt/stacks
    environment:
      - DOCKGE_STACKS_DIR=/opt/stacks
```

Launch the service using the Docker Compose plugin:
```bash
cd /opt/dockge
docker compose up -d
```

---

## 3. Diagnostics & Validation

Verify process status, resource allocation, and port listening state:

```bash
docker ps --filter "name=dockge" --format "table {{.Names}}	{{.Status}}	{{.Ports}}"
```

### Expected Output
```text
NAMES     STATUS         PORTS
dockge    Up 2 minutes   0.0.0.0:5001->5001/tcp, :::5001->5001/tcp
```

Inspect memory footprint via container runtime statistics:
```bash
docker stats --no-stream dockge --format "table {{.Name}}	{{.MemUsage}}	{{.CPUPerc}}"
```

### Expected Output
```text
NAME      MEM USAGE / LIMIT     CPU %
dockge    18.4MiB / 3.65GiB     0.02%
```

---

## 4. Best Practices (Do's and Don'ts)

* **DO:**
  * Maintain all production Compose files inside `/opt/stacks/<service_name>/compose.yaml` to ensure full Dockge UI compatibility.
  * Enforce daemon log rotation in `/etc/docker/daemon.json` (`max-size: 10m`, `max-file: 2`) to protect small solid-state drives.
  * Use SQLite backup routines or filesystem snapshots for `/opt/dockge/data`.

* **DON'T:**
  * Do NOT mount `/opt/stacks` across network filesystems (NFS/CIFS) with unmapped file locking mechanisms.
  * Do NOT use Portainer on memory-starved machines when only Compose management is required.
  * Do NOT leave Docker socket `/var/run/docker.sock` exposed outside internal network namespaces.
