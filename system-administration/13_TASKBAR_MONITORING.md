# 13: Taskbar Performance Monitoring

This guide covers the implementation of real-time hardware telemetry (CPU, RAM, and Network speeds) directly in the GNOME top panel using the Extension Manager.

## Implementation: Extension Manager

Unlike the standard windowed System Monitor, this method utilizes the **Extension Manager** GUI to install a resident applet for the taskbar.

### 1. Install the Manager
Install the GUI utility that handles the search and installation of GNOME Shell extensions:
```bash
sudo apt update && sudo apt install gnome-shell-extension-manager -y
```

### 2. Integration Protocol
1. Open **Extension Manager** from the application menu.
2. Navigate to the **Browse** tab.
3. Search for **"Vitals"** or **"System-monitor"**.
4. Click **Install**.
5. Once active, the "app" will appear in the top taskbar showing real-time stats.

## Configuration and Features

Once installed, the extension provides highly granular control over what is displayed in the taskbar:

* **CPU/RAM Usage**: Real-time percentage and memory load.
* **Network Throughput**: Instantaneous download and upload speeds (B/s, KB/s, or MB/s).
* **Thermal Monitoring**: Hardware temperature readouts (if supported by kernel sensors).
* **Refresh Interval**: Adjustable polling frequency to balance accuracy vs. system overhead.

*(Note: If sensor data for temperatures is missing, ensure `lm-sensors` is installed via `sudo apt install lm-sensors`).*