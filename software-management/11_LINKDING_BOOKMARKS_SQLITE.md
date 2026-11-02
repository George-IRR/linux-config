# 11: Linkding Bookmark Manager & iOS REST Integration

Deployment of the lightweight Linkding bookmarking platform utilizing SQLite embedded storage (<40MB RAM footprint) and integration with iOS native share-sheet extensions via REST API authentication.

---

## 1. Storage Provisioning & Stack Deployment

Provision dedicated volume path for SQLite database persistence:

```bash
sudo mkdir -p /opt/stacks/linkding/data
sudo chown -R $USER:$USER /opt/stacks/linkding
```

Define the Docker Compose specification in `/opt/stacks/linkding/compose.yaml`:

```yaml
services:
  linkding:
    image: sissbruecker/linkding:latest
    container_name: linkding
    restart: unless-stopped
    ports:
      - "8020:9090"
    volumes:
      - /opt/stacks/linkding/data:/etc/linkding/data
```

Deploy the stack:
```bash
cd /opt/stacks/linkding
docker compose up -d
```

---

## 2. Superuser Provisioning & iOS REST API Pairing

Generate initial administrative account without exposing interactive ports:

```bash
docker exec -it linkding python manage.py createsuperuser
```

### iOS Client Authentication Setup
1. Access the web interface at `https://<hostname>.<tailnet>.ts.net:8444` (or local port 8020).
2. Authenticate and navigate to **Settings** -> **Integrations**.
3. Generate and copy the **REST API Authentication Token**.
4. In the iOS Linkding third-party client (or Apple Shortcuts workflow):
   * Set **Server URL** to `https://<hostname>.<tailnet>.ts.net:8444`.
   * Set **API Token** to `<auth-token>`.

---

## 3. Diagnostics & Validation

Query Linkding's REST endpoint via curl using Bearer token authentication:

```bash
curl -s -H "Authorization: Token <auth-token>"   http://localhost:8020/api/bookmarks/?limit=1 | grep -o '"count":[0-9]*'
```

### Expected Output
```text
"count":0
```

Inspect process status and memory allocation:
```bash
docker stats --no-stream linkding --format "table {{.Name}}	{{.MemUsage}}"
```

### Expected Output
```text
NAME        MEM USAGE / LIMIT
linkding    34.1MiB / 3.65GiB
```

---

## 4. Best Practices (Do's and Don'ts)

* **DO:**
  * Implement periodic automated backups of `/opt/stacks/linkding/data/db.sqlite3` using atomic SQLite `.backup` commands.
  * Enable Tailscale on the iOS client device to ensure remote bookmark synchronization without opening public firewall ports.
  * Configure asset archival flags if full offline text preservation is required.

* **DON'T:**
  * Do NOT use external PostgreSQL or MySQL containers for single-user bookmarking; SQLite avoids ~150MB of database memory overhead.
  * Do NOT share or commit API tokens to version control.
  * Do NOT mount the SQLite database directory over network file shares prone to CIFS/NFS locking issues.
