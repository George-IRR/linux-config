# 12: Wake-on-LAN and Remote LUKS Unlock via Dropbear Initramfs

Operational workflow for powering on an encrypted workstation remotely via Wake-on-LAN (WoL) from an always-on LAN bastion host (`<server-host>`), unlocking its LUKS2 root partition pre-boot over SSH using `dropbear-initramfs`, and establishing bidirectional SSH access over both LAN and Tailscale.

---

## 1. Bidirectional SSH Access from Bastion to Workstation

When `<client-host>` can already reach `<server-host>`, configure reverse passwordless SSH access so `<server-host>` can act as a local jump host for both WoL triggers and pre-boot LUKS unlocking.

1. On `<server-host>`, generate a dedicated Ed25519 keypair:
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "server-to-desktop"
   ```

2. On `<server-host>`, create `~/.ssh/config` with profiles for LAN, Tailscale fallback, and pre-boot Dropbear unlocking:
   ```ini
   Host <client-host>
       HostName <client-ip>
       User <user>
       IdentityFile ~/.ssh/id_ed25519

   Host <client-host>-ts
       HostName <tailscale-ip>
       User <user>
       IdentityFile ~/.ssh/id_ed25519

   Host <client-host>-unlock
       HostName <client-ip>
       Port 2222
       User root
       IdentityFile ~/.ssh/id_ed25519
   ```
   - `Port 2222`: Isolates the initramfs Dropbear SSH host key from the normal OS OpenSSH host key on port `22`, preventing `known_hosts` mismatch errors.

3. Set strict permissions on `~/.ssh/config` and append `<server-host>`'s public key (`<ssh-public-key>`) to `~/.ssh/authorized_keys` on `<client-host>`:
   ```bash
   chmod 600 ~/.ssh/config
   # On <client-host>:
   echo "<ssh-public-key>" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

---

## 2. Persistent Wake-on-LAN on Workstation

Enable Magic Packet (`g`) wake support in both the OS network profile and motherboard firmware.

1. Identify the primary wired interface and MAC address on `<client-host>`:
   ```bash
   ip link show <interface>
   ```

2. Enable Wake-on-LAN persistently via NetworkManager and apply immediately with `ethtool`:
   ```bash
   sudo nmcli connection modify netplan-<interface> 802-3-ethernet.wake-on-lan magic
   sudo ethtool -s <interface> wol g
   ```
   - `802-3-ethernet.wake-on-lan magic`: Ensures the NIC stays armed for Magic Packets across reboots and shutdowns.

3. Enable **Wake on LAN / Power On by PCI-E** in the `<client-host>` BIOS/UEFI firmware settings (and disable ErP/EuP deep power-down if present, as it cuts standby NIC power).

---

## 3. Wake-on-LAN Trigger Script on Bastion

Use a zero-dependency Python 3 script on `<server-host>` to broadcast a Layer-2/UDP Magic Packet to `<client-host>` on the local subnet.

1. Create `~/wake-desktop.py` on `<server-host>`:
   ```python
   #!/usr/bin/env python3
   import socket

   MAC = "<mac-address>"
   BROADCAST = "192.168.1.255"
   PORT = 9

   mac_bytes = bytes.fromhex(MAC.replace(":", "").replace("-", ""))
   packet = b"\xff" * 6 + mac_bytes * 16

   with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
       s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
       s.sendto(packet, (BROADCAST, PORT))

   print(f"Magic packet sent to {MAC} via {BROADCAST}:{PORT}")
   ```

2. Make the script executable:
   ```bash
   chmod +x ~/wake-desktop.py
   ```

---

## 4. Pre-Boot LUKS Unlock via `dropbear-initramfs`

Install and configure `dropbear-initramfs` on `<client-host>` so an SSH listener starts before the root filesystem is decrypted.

1. Install `dropbear-initramfs`:
   ```bash
   sudo apt update && sudo apt install -y dropbear-initramfs
   ```

2. Authorize `<server-host>`'s public key for pre-boot `root` unlock:
   ```bash
   sudo install -m 600 /dev/null /etc/dropbear/initramfs/authorized_keys
   echo "<ssh-public-key>" | sudo tee /etc/dropbear/initramfs/authorized_keys >/dev/null
   ```

3. Configure Dropbear options in `/etc/dropbear/initramfs/dropbear.conf`:
   ```bash
   sudo tee /etc/dropbear/initramfs/dropbear.conf >/dev/null <<'EOF'
   DROPBEAR_OPTIONS="-I 180 -j -k -p 2222 -s -c cryptroot-unlock"
   EOF
   ```
   - `-I 180`: Idle timeout of 180 seconds.
   - `-j -k`: Disables local and remote SSH port forwarding in initramfs.
   - `-s`: Disables password authentication (key-only).
   - `-c cryptroot-unlock`: Forces the SSH session directly into the LUKS passphrase prompt.

4. Assign a static IP in `/etc/initramfs-tools/conf.d/network` so `<client-host>` is immediately reachable at `<client-ip>` during early boot:
   ```bash
   sudo tee /etc/initramfs-tools/conf.d/network >/dev/null <<'EOF'
   IP=<client-ip>::<gateway-ip>:255.255.255.0:<client-host>:<interface>:off
   EOF
   ```

5. Rebuild the initramfs image:
   ```bash
   sudo update-initramfs -u
   ```

---

## 5. Diagnostics & Validation

Verify WoL capability, initramfs generation, and the full remote wake-and-unlock workflow.

1. Check Wake-on-LAN status on `<client-host>`:
   ```bash
   sudo ethtool <interface> | grep -i wake-on
   ```
   Expected Output:
   ```text
   	Supports Wake-on: pumbg
   	Wake-on: g
   ```

2. Verify `initramfs` rebuild completed without errors:
   ```bash
   sudo update-initramfs -u
   ```
   Expected Output:
   ```text
   update-initramfs: Generating /boot/initrd.img-<kernel-version>-generic
   ```

3. Test end-to-end from a remote device (via Tailscale):
   ```bash
   ssh <server-host>
   ~/wake-desktop.py
   # Wait 10-15 seconds for initramfs network + Dropbear
   ssh <client-host>-unlock
   # Enter LUKS passphrase; session closes automatically on unlock
   # Wait 10-15 seconds for full OS boot
   ssh <client-host> "hostname && whoami"
   ```
   Expected Output:
   ```text
   <client-host>
   <user>
   ```

---

## 6. Best Practices (Do's and Don'ts)

* **Do** isolate Dropbear on a non-standard port (e.g., `2222`) so its host key never conflicts with the OS OpenSSH server on port `22`.
* **Do** enforce `-s` (disable password logins) and `-j -k` (disable port forwarding) in `DROPBEAR_OPTIONS`.
* **Do** keep `<server-host>` on the same Layer-2 broadcast domain as `<client-host>`, since WoL Magic Packets do not traverse routed subnets or Tailscale tunnels by default.
* **Don't** share the same SSH host key or `known_hosts` entry between port `22` and port `2222`.
* **Don't** forget to run `sudo update-initramfs -u` after any edit to `/etc/dropbear/initramfs/` or `/etc/initramfs-tools/`; changes will not take effect at boot otherwise.
