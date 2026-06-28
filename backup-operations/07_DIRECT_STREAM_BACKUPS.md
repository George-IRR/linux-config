# 07: Direct-Stream Container Backups with Zero Footprint

A technical guide for implementing a streaming backup infrastructure on resource-constrained storage nodes (e.g., Raspberry Pi Zero 2W). This system archives live databases and streams files directly to cloud targets via `rclone rcat` without write operations to the local storage or local RAM buffers.

---

## 1. Architectural Concept

Traditional backup methodologies write a compressed archive (`.tar.gz`, `.xz`, or `.zpaq`) to local disk or a RAM disk (`/dev/shm`) before uploading the file to a cloud provider. On systems with constrained hardware (512MB RAM and wear-prone MicroSD cards), this causes major issues:
* **Storage Exhaustion:** If the source directory is large, writing a temporary archive can easily exceed available disk space.
* **OOM Kill Crashes:** Utilizing RAM disks blocks memory needed by operational system tasks, triggering the Linux Out-Of-Memory (OOM) killer.
* **MicroSD Wear:** Constant disk write operations reduce the lifespan of cheap flash storage cards.

### The Solution: Pipeline Streaming
By combining standard archiving tool streams with `rclone rcat` (remote cat), we can compress files on the fly and push the stream straight to cloud targets over network sockets:

```text
[ Filesystem ] ---> [ tar ] ---> [ XZ Compression ] ---> [ rclone rcat ] ---> [ Cloud Storage ]
```
*Local Disk Writes:* **0 bytes** *Local RAM Overhead:* **Less than 10MB**

---

## 2. Ensuring SQLite Database Consistency

Vaultwarden stores its records in a flat SQLite database (`db.sqlite3`). If you copy this file while the application is actively writing to it, the resulting backup can suffer from **page corruption** or **unbalanced indexes**.

To prevent this without shutting down services or spawning heavy transaction-journaling dumps:
1. Trigger `podman pause vaultwarden` to freeze the application's runtime threads. SQLite locks are guaranteed to remain static.
2. Read the directory and stream the data.
3. Trigger `podman unpause vaultwarden` once the archiving stream initializes. The freeze lasts less than 3 seconds.

---

## 3. Deployment Script: `vaultwarden_backup_script.sh`

This script runs a weekly automated backup. It tracks elapsed time using a localized UNIX timestamp file, ensuring backups occur exactly every 7 days, even if the Raspberry Pi is rebooted or suffers unexpected power loss.

[Copy this script](./../scripts/vaultwarden_backup_script.sh) to `/home/<YOUR_USERNAME>/vaultwarden_backup_script.sh`


### Make the Script Executable
```bash
chmod +x /home/<YOUR_USERNAME>/vaultwarden_backup_script.sh
```

---

## 4. Disaster Recovery (Restore Protocol)

Because the backup is streamed to the cloud, restoring it requires reversing the stream. The cloud file is read, decompressed, and written to the system in a single line of command.

1. Stop any active container instances:
   ```bash
   podman stop vaultwarden
   ```
2. Pull the archive from the cloud and extract it directly to the root filesystem structure:
   ```bash
   rclone --config /home/<YOUR_USERNAME>/.config/rclone/rclone.conf cat "<YOUR_RCLONE_REMOTE_NAME>:<YOUR_REMOTE_CLOUD_PATH>/vaultwarden_direct_XXXXXXXX_XXXXXX.tar.xz" | tar -xJf - -C /
   ```
   * `-C /` ensures the relative archive path extracts correctly back to its target.
3. Start the container:
   ```bash
   podman start vaultwarden
   ```

---

## 5. Security Architecture (Decryption on Untrusted Environments)

Vaultwarden relies on client-side, zero-knowledge architecture. All cryptographic operations occur on your end device (iPhone/PC). Lacking the master password, a compromised SQLite database exposes zero readable secrets.

To read or verify files on an external PC:
1. Download the backup file from your cloud provider.
2. Extract the contents using any file manager (such as 7-Zip on Windows or terminal command on Linux):
   ```bash
   tar -xJf vaultwarden_direct_XXXXXXXX_XXXXXX.tar.xz
   ```
3. Use **DB Browser for SQLite** to open `db.sqlite3`. You will notice all entries in the `ciphers` table are fully encrypted using AES-256 blocks, proving complete data security.