# 03: Hardened SSH Infrastructure

Operational baseline for migrating remote Linux hosts from password-based logins to asymmetric Ed25519 cryptographic authentication, structured client alias profiles, and localized UFW network firewalling.

---

## 1. Asymmetric Key Generation & Deployment

Generate a dedicated Ed25519 keypair on `<client-host>` and deploy the public key to `<server-host>`.

1. Generate the keypair with a descriptive comment:
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/<key-name> -C "<user>@<client-host>"
   ```

2. Copy the public key to `<server-host>`:
   ```bash
   ssh-copy-id -i ~/.ssh/<key-name>.pub <user>@<server-ip>
   ```

---

## 2. Client Alias Profiles (`~/.ssh/config`)

Define explicit host aliases on `<client-host>` to standardize usernames, target IPs, and identity files.

1. Append the host block to `~/.ssh/config`:
   ```ini
   Host <server-host>
       HostName <server-ip>
       User <user>
       IdentityFile ~/.ssh/<key-name>
       IdentitiesOnly yes
   ```
   - `IdentitiesOnly yes`: Prevents the SSH client from offering unrelated keys loaded in `ssh-agent` before `<key-name>`.

2. Enforce strict file permissions:
   ```bash
   chmod 600 ~/.ssh/config
   ```

---

## 3. Server Daemon Hardening (`/etc/ssh/sshd_config.d/`)

Disable password logins and root password access on `<server-host>` once key-based login is verified.

1. Create a drop-in configuration file:
   ```bash
   sudo tee /etc/ssh/sshd_config.d/99-hardening.conf >/dev/null <<'EOF'
   PasswordAuthentication no
   KbdInteractiveAuthentication no
   PubkeyAuthentication yes
   PermitRootLogin prohibit-password
   EOF
   ```

2. Validate syntax and reload `sshd`:
   ```bash
   sudo sshd -t && sudo systemctl reload ssh
   ```

---

## 4. Localized Firewall Restriction (`ufw`)

Restrict SSH port `22/tcp` on `<server-host>` to trusted LAN or VPN subnets.

1. Allow SSH only from `<client-ip>` (or the trusted subnet `192.168.1.0/24`):
   ```bash
   sudo ufw allow from <client-ip> to any port 22 proto tcp
   sudo ufw enable
   ```

---

## 5. Diagnostics & Validation

Verify daemon configuration, key-only login, and active firewall rules.

1. Test `sshd` configuration syntax and effective settings:
   ```bash
   sudo sshd -T | grep -E 'passwordauthentication|pubkeyauthentication|permitrootlogin'
   ```
   Expected Output:
   ```text
   pubkeyauthentication yes
   passwordauthentication no
   permitrootlogin prohibit-password
   ```

2. Verify passwordless login from `<client-host>`:
   ```bash
   ssh -o BatchMode=yes <server-host> "hostname"
   ```
   Expected Output:
   ```text
   <server-host>
   ```

---

## 6. Best Practices (Do's and Don'ts)

* **Do** test key-based authentication in a second terminal before closing your active session after disabling `PasswordAuthentication`.
* **Do** place custom overrides in `/etc/ssh/sshd_config.d/` rather than editing `/etc/ssh/sshd_config` directly.
* **Don't** enable `ufw` remotely without first allowing SSH (`22/tcp`) from your management IP or subnet.
