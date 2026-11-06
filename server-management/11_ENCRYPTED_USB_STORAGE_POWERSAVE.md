# 11: Encrypted Secondary USB Storage with Auto-Mount & Autosuspend Tuning

Operational workflow for configuring an auxiliary USB flash drive with LUKS2 encryption, chained securely to the primary TPM-encrypted root partition via a protected keyfile, accompanied by USB autosuspend and ext4 commit tuning to minimize thermal wear on compact flash hardware.

---

## 1. Keyfile Generation on Encrypted Root

Store the cryptographic unlock secret strictly on the encrypted primary storage volume. If the physical drive is disconnected from the host, the partition remains completely inaccessible.

1. Create a dedicated key directory with strict root-only permissions:
   ```bash
   sudo mkdir -p /etc/cryptsetup-keys.d
   ```
2. Generate a 512-byte cryptographically secure random key:
   ```bash
   sudo dd if=/dev/urandom of=/etc/cryptsetup-keys.d/usbstick.key bs=512 count=1
   sudo chmod 0400 /etc/cryptsetup-keys.d/usbstick.key
   ```

---

## 2. Partition Encryption and Filesystem Initialization

Locate the target USB block device (e.g., `/dev/sdb1`) via `lsblk` and format with LUKS2.

1. Format the target partition using the keyfile:
   ```bash
   sudo cryptsetup luksFormat /dev/sdb1 --key-file /etc/cryptsetup-keys.d/usbstick.key
   ```
   *Note: Type `YES` in capital letters when prompted to confirm destruction of existing data.*

2. Add a manual passphrase as an auxiliary recovery keyslot:
   ```bash
   sudo cryptsetup luksAddKey /dev/sdb1 --key-file /etc/cryptsetup-keys.d/usbstick.key
   ```

3. Open the encrypted container and format with `ext4`:
   ```bash
   sudo cryptsetup open /dev/sdb1 usbstick_crypt --key-file /etc/cryptsetup-keys.d/usbstick.key
   sudo mkfs.ext4 -L USB_STORAGE /dev/mapper/usbstick_crypt
   sudo mkdir -p /mnt/usbstick_storage
   ```

---

## 3. Automated Decryption and Mounting Configuration

1. Capture the partition UUID:
   ```bash
   UUID_STICK=$(sudo blkid -s UUID -o value /dev/sdb1)
   ```

2. Register the device in `/etc/crypttab` with the `nofail` flag to allow boot continuation if the drive is unplugged:
   ```bash
   echo "usbstick_crypt UUID=${UUID_STICK} /etc/cryptsetup-keys.d/usbstick.key luks,nofail" | sudo tee -a /etc/crypttab
   ```

3. Register the filesystem in `/etc/fstab` with `noatime` and `commit=60` to buffer journal metadata in RAM and reduce periodic flash writes:
   ```bash
   echo "/dev/mapper/usbstick_crypt /mnt/usbstick_storage ext4 defaults,noatime,commit=60,nofail 0 2" | sudo tee -a /etc/fstab
   ```

4. Reload systemd mount units and mount the directory:
   ```bash
   sudo systemctl daemon-reload
   sudo mount /mnt/usbstick_storage
   sudo chown -R $USER:$USER /mnt/usbstick_storage
   ```

---

## 4. USB Autosuspend & Thermal Power Optimization

Compact metal USB 3.0 flash drives run hot due to continuous controller activity. Enable kernel runtime power management and autosuspend to idle the USB physical layer during inactivity.

1. Create a persistent udev rule for USB device autosuspend:
   ```bash
   sudo bash -c 'cat << "EOF" > /etc/udev/rules.d/50-usb-autosuspend.rules
   ACTION=="add", SUBSYSTEM=="usb", TEST=="power/control", ATTR{power/control}="auto"
   ACTION=="add", SUBSYSTEM=="usb", TEST=="power/autosuspend_delay_ms", ATTR{power/autosuspend_delay_ms}="2000"
   EOF'
   ```

2. Trigger the new rules:
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

3. Install and enable the system power management daemon:
   ```bash
   sudo apt install -y tlp
   sudo systemctl enable --now tlp
   sudo systemctl disable NetworkManager-wait-online.service
   sudo tlp start
   ```

---

## 5. Diagnostics & Validation

### Validate Mount Status and Available Capacity
```bash
df -h /mnt/usbstick_storage
```

#### Expected Output
```text
Filesystem                  Size  Used Avail Use% Mounted on
/dev/mapper/usbstick_crypt  114G  2.1M  108G   1% /mnt/usbstick_storage
```

### Validate Runtime Power Control
```bash
sudo tlp-stat -u | grep -E "Bus|Device|Control" | head -n 10
```

#### Expected Output
```text
...
Device ...: power/control = auto, power/autosuspend_delay_ms = 2000
```

---

## 6. Best Practices (Do's and Don'ts)

### Do's
- Always include `nofail` in both `/etc/crypttab` and `/etc/fstab` for removable media. Without it, a missing USB drive drops the entire machine into emergency mode during boot.
- Use `noatime` and `commit=60` for all flash-based media to prevent thermal throttling and wear leveling exhaustion.
- Store databases, logs, and container state on the internal SSD; use the flash drive predominantly for static sequential media (music, videos, archives).

### Don'ts
- Do not store the keyfile on unencrypted partitions such as `/boot` or `/boot/efi`.
- Do not run high-IOPS SQLite or transaction databases directly on consumer USB flash drives.
