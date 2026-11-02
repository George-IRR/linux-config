# 08: Tailscale Serve HTTPS & Automated TLS Termination

Implementation of encrypted HTTPS endpoints and automated Let's Encrypt certificate lifecycle management via native Tailscale Serve, eliminating the overhead of dedicated reverse proxy containers on low-RAM hosts.

---

## 1. Prerequisites and Tailnet HTTPS Provisioning

Tailscale Serve relies on Tailscale MagicDNS and machine-specific Fully Qualified Domain Names (FQDN).

1. Ensure MagicDNS and HTTPS Certificates are enabled in the Tailscale Admin Console under the **DNS** settings.
2. Confirm the host machine is authenticated and active within the tailnet:
   ```bash
   sudo tailscale status
   ```
3. Verify local resolution of the machine FQDN:
   ```bash
   tailscale status --json | grep -i "DNSName"
   ```

---

## 2. Service Exposure Configuration

Map internal HTTP ports to public tailnet HTTPS listeners running as background daemons.

### A. Primary Web Dashboard (Port 443 Default)
Bind the internal dashboard service (e.g., Homer on port 8010) to the standard HTTPS port:
```bash
sudo tailscale serve --bg 8010
```

### B. Secondary Administrative Services (Custom HTTPS Ports)
Bind administrative interfaces (e.g., Dockge on port 5001, Linkding on port 8020) to dedicated TLS listeners:
```bash
# Expose Docker management interface on HTTPS 8443
sudo tailscale serve --bg --https=8443 5001

# Expose bookmark archive interface on HTTPS 8444
sudo tailscale serve --bg --https=8444 8020
```

---

## 3. Diagnostics & Validation

Query the active Serve proxy tables to confirm TLS termination paths and upstream bindings:

```bash
tailscale serve status
```

### Expected Output
```text
https://<hostname>.<tailnet>.ts.net/ (tailnet only)
|-- / proxy http://127.0.0.1:8010

https://<hostname>.<tailnet>.ts.net:8443 (tailnet only)
|-- / proxy http://127.0.0.1:5001

https://<hostname>.<tailnet>.ts.net:8444 (tailnet only)
|-- / proxy http://127.0.0.1:8020
```

Validate TLS handshake and HTTP response headers from an authenticated client:
```bash
curl -Iv https://<hostname>.<tailnet>.ts.net/
```

### Expected Output
```text
* Connected to <hostname>.<tailnet>.ts.net (100.X.Y.Z) port 443
* ALPN: offers h2,http/1.1
* SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256
* Server certificate:
*  subject: CN=<hostname>.<tailnet>.ts.net
*  issuer: C=US; O=Let's Encrypt; CN=R3
< HTTP/2 200
```

---

## 4. Best Practices (Do's and Don'ts)

* **DO:**
  * Use `--bg` to ensure Serve proxy handlers persist across user terminal disconnections.
  * Update Homer configuration files with exact `https://<hostname>.<tailnet>.ts.net:<port>` endpoints to avoid mixed-content browser blocks.
  * Reset corrupt or misrouted listener mappings cleanly with `sudo tailscale serve reset`.

* **DON'T:**
  * Do NOT deploy heavy containerized proxies (Nginx Proxy Manager, Traefik) when memory constraints (<4GB RAM) dictate keeping system overhead under 50MB.
  * Do NOT expose plain HTTP over the tailnet if client applications enforce browser Secure Contexts (e.g., WebCrypto, Bitwarden API).
  * Do NOT hardcode personal machine names or cleartext auth tokens in committed scripts.
