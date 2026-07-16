## 01: SideStore & LiveContainer Implementation on iOS 18.2

Technical documentation for establishing an untethered, PC-free application sideloading environment. This protocol resolves specific iOS 18.2 network loopback restrictions, cryptographic pairing failures, and Linux USB multiplexing conflicts.

## 1. Linux Host Preparation & USB Multiplexer Hardening

Ubuntu utilizes automated media daemons (GVfs/PTP) that intercept iOS USB connections, blocking the `usbmuxd` socket required for cryptographic pairing. These must be terminated.

### 1.1 Clear Legacy Pairing Keys

Purge the system lockdown database to prevent signature mismatch errors:

```bash
sudo rm -rf /var/lib/lockdown/*

```

### 1.2 Terminate Conflicting Daemons

Kill automated volume monitors and restart the USB multiplexer daemon:

```bash
killall gvfsd-gphoto2 gvfs-gphoto2-volume-monitor 2>/dev/null
sudo systemctl restart usbmuxd

```

### 1.3 Establish Trust Protocol

1. Connect the iOS device via USB.
2. Unlock the device.
3. Accept the **Trust This Computer** prompt and enter the device PIN.

## 2. Cryptographic Pairing File Generation (iLoader)

SideStore requires an XML-formatted cryptographic pairing file containing the `EscrowBag` key to simulate a local signing server. This protocol uses `iLoader` strictly for file generation, bypassing broken automated transfer functions.

### 2.1 Execute iLoader with Wayland/GNOME Compatibility

Bypass `EGL_BAD_PARAMETER` graphical subsystem crashes by forcing X11 compatibility variables:

```bash
GIO_MODULE_DIR="" QT_QPA_PLATFORM=xcb ./iloader-linux-amd64.AppImage

```

### 2.2 Generate and Export File

1. Within the iLoader graphical interface, navigate to the **Manage pairing file** utility.
2. Execute the generation process. The application extracts the correctly formatted XML file containing the device UDID.
3. Export the file to the local Linux filesystem.

### 2.3 Transfer to iOS Device

Host a temporary local Python web server to securely transfer the file to the iOS device without relying on cloud intermediaries:

```bash
cd /path/to/exported/file
python3 -m http.server 8080

```

* Access `http://[LINUX_HOST_IP]:8080` via Safari on the iOS device.
* Download the file.
* **Critical:** Open the iOS **Files** application. Inspect the filename. If iOS appended a hidden extension (e.g., `filename.mobiledevicepairing.txt`), rename the file and delete the `.txt` suffix.

## 3. iOS 18.2 Network Loopback Architecture

iOS 18.2 enforces rigid security parameters that block application loopback requests under specific network states.

### 3.1 Mandatory Network State

SideStore will throw a `Failed to Refresh` error if the device operates exclusively on Cellular Data (5G/LTE/4G).

* **Requirement:** An active Wi-Fi connection is mandatory to open the internal network interface. If no router is available, enabling **Personal Hotspot** forces the interface open.

### 3.2 VPN Configuration (LocalDevVPN)

Standard WireGuard profiles present routing instabilities on iOS 18.2.

1. Install **LocalDevVPN** from the App Store (Developer: Coxson Engineering LLC).
2. Launch the application and execute **Connect**. Input the device PIN to authorize the VPN profile.
3. Navigate to **Settings > Privacy & Security > Local Network**. Ensure permissions are explicitly granted for both **SideStore** and **LocalDevVPN**.

## 4. SideStore Initialization & Anisette Configuration

1. Activate the **LocalDevVPN** connection.
2. Launch **SideStore**.
3. When prompted, select the `.mobiledevicepairing` file transferred in Step 2.3.
4. **Anisette Configuration:** If login fails with `error -45003 (invalid Trust Key)`, the default public Anisette server is blocked by Apple.
* Navigate to SideStore Settings.
* Modify the Anisette URL to a functional public endpoint (e.g., `[https://anisette.sidestore.io](https://anisette.sidestore.io)` or `[https://anisette.esign.yyyue.best](https://anisette.esign.yyyue.best)`), or deploy a local Docker Anisette V3 container and input the local IP.


5. Execute **Refresh All** to validate the signing certificate.

## 5. LiveContainer Sandboxed Data Migration

Applications installed within LiveContainer run off the host application's signature. Uninstalling the previous LiveContainer instance deletes all internal app data. Follow this strict protocol to migrate data to the SideStore-signed instance.

### 5.1 Backup Phase

1. Open the iOS **Files** app.
2. Navigate to **On My iPhone**.
3. Copy the existing `LiveContainer` root directory.
4. Paste the directory into an external secure location (e.g., iCloud Drive or a distinct local folder).

### 5.2 Deployment Phase

1. Delete the legacy LiveContainer application from the iOS home screen.
2. Sideload the `LiveContainer.ipa` payload via SideStore.
3. Launch the newly installed LiveContainer application once to initialize its internal directory hierarchy. Force-close it via the App Switcher.

### 5.3 Restoration Phase

1. Copy the backup directory secured in Phase 5.1.
2. Navigate to **On My iPhone** and paste the directory.
3. Select **Replace** for all resulting file conflicts. This overwrites the blank initialization structure with the historical sandbox data.