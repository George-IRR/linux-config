# 10: LUKS Full-Disk Encryption TPM2 Auto-Unlock & Hardware Hardening (HP T630)

Technical runbook for configuring unattended LUKS2 disk auto-unlock using TPM 2.0 via Clevis on Debian, coupled with physical hardware hardening on HP Thin Client T630 hardware through BIOS security policies, GRUB PBKDF2 authentication, and unrestricted default boot chaining.

---

## 1. System Requirements & TPM2 Enrollment

Verify that the TPM 2.0 controller is detected by the kernel and install the required userspace abstraction libraries and Clevis hooks.

1. Verify hardware detection of the TPM device:
   ```bash
   ls -l /dev/tpm*
   ```
2. Install Clevis with TPM2 and initramfs integration:
   ```bash
   sudo apt update
   sudo apt install -y clevis clevis-luks clevis-tpm2 clevis-initramfs tpm2-tools
   ```
3. Bind the encrypted LUKS partition (e.g., `/dev/sda3`) to the local TPM 2.0 security chip:
   ```bash
   sudo clevis luks bind -d /dev/sda3 tpm2 '{}'
   ```
   *Note: Enter the existing manual LUKS passphrase when prompted.*

4. Rebuild all initramfs images to incorporate Clevis unlock hooks:
   ```bash
   sudo update-initramfs -u -k all
   ```

---

## 2. Crypttab Verification & Cleanup

Ensure `/etc/crypttab` remains strictly standard. Do not add `tpm2-device=auto` when using Clevis with Debian's `initramfs-tools` to avoid parser warnings.

```text
# Correct format inside /etc/crypttab
sda3_crypt UUID=<partition-uuid> none luks,discard,x-initrd.attach
```

---

## 3. GRUB Hardening: Unrestricted Default Boot with Protected Editing

Prevent attackers with physical machine access from appending `init=/bin/bash` or `single` at the bootloader prompt, while retaining unattended automatic reboots.

1. Generate a salted PBKDF2 hash for the GRUB administrator:
   ```bash
   grub-mkpasswd-pbkdf2
   ```
2. Configure the administrative user in `/etc/grub.d/40_custom`:
   ```ini
   set superusers="admin"
   password_pbkdf2 admin grub.pbkdf2.sha512.REDACTED_PBKDF2_HASH_STRING
   ```
3. Modify `/etc/grub.d/10_linux` so default kernels boot without password prompts, requiring authentication only when attempting to edit (`e`) or enter recovery:
   ```bash
   sudo sed -i 's/CLASS="--class gnu-linux/CLASS="--unrestricted --class gnu-linux/' /etc/grub.d/10_linux
   sudo update-grub
   ```

---

## 4. HP Thin Client T630 BIOS Hardening

Access BIOS setup via **F10** during system power-on and configure the following hardware policies:

1. **Setup Password:** Set a strong administrative password under `Security` to lock firmware configuration.
2. **Power-On Password:** Leave **Disabled** to guarantee headless, automated reboots after power outages.
3. **Boot Order:**
   - Place internal storage (`Debian`) as first priority.
   - Disable all USB and Network PXE boot sources.
4. **Password Options:**
   - `Password prompt on F9 & F12`: **Enabled** (intercepts manual boot overrides).
   - `Setup Browse Mode`: **Disabled**.
   - `Stringent Password`: **Disabled** (avoids bricking the board if the setup password is lost).
5. **Secure Boot:** **Enabled** (preserves kernel and boot shim validation).

---

## 5. Diagnostics & Validation

### Validate Clevis Token Inclusion in Initramfs
```bash
lsinitramfs /boot/initrd.img-$(uname -r) | grep clevis
```

#### Expected Output
```text
scripts/local-bottom/clevis
scripts/local-top/clevis
usr/bin/clevis
usr/bin/clevis-decrypt-tpm2
usr/bin/clevis-luks-unlock
```

### Validate Unrestricted GRUB Declaration
```bash
sudo grep -m 1 "menuentry 'Debian" /boot/grub/grub.cfg
```

#### Expected Output
```text
menuentry 'Debian GNU/Linux' --class debian --unrestricted --class gnu-linux --class gnu --class os ...
```

---

## 6. Best Practices (Do's and Don'ts)

### Do's
- Keep the master LUKS passphrase archived in an off-site password vault. TPM binding functions as an access token, not a replacement for recovery keys.
- Enforce SSH key-only authentication (`PasswordAuthentication no` in `/etc/ssh/sshd_config`) so that a stolen, automatically decrypted host exposes no remote shell attack vectors.
- Set `UseDNS no` in `/etc/ssh/sshd_config.d/` to prevent connection delays during headless restarts.

### Don'ts
- Do not enable `Power-On Password` in BIOS; doing so halts server boot until a physical keyboard enters credentials.
- Do not store plain text passwords in `/etc/grub.d/40_custom`; always use `password_pbkdf2`.
- Do not discard the recovery jumper procedure knowledge; clearing CMOS resets the TPM state on HP hardware, requiring the manual LUKS passphrase to re-enroll.
