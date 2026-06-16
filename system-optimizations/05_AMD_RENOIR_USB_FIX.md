# 05: AMD Renoir xHCI USB Controller Fix

Documentation for mitigating catastrophic USB subsystem failures caused by AMD Renoir xHCI host controller state-machine lockups under heavy endpoint load.

## Problem Profile
When connecting multiple composite USB devices (such as dual nRF development boards exposing CDC-ACM serial outputs and virtual Mass Storage Volumes simultaneously), the integrated AMD Renoir xHCI controller (`0000:04:00.3`) crashes under endpoint scheduling latency. 

### Failure Signature (dmesg)
```text
xhci_hcd 0000:04:00.3: xHCI host not responding to stop endpoint command
xhci_hcd 0000:04:00.3: xHCI host controller not responding, assume dead
xhci_hcd 0000:04:00.3: HC died; cleaning up
```
When this occurs, the entire physical root hub goes offline, disabling both data translation targets and system Human Interface Devices (e.g., USB mouse).

---

## Technical Remedies

### 1. Hard Reset the Wedged PCI Controller (Runtime Recovery)
Execute a hardware-level unbind and reset sequence over the PCIe bus to restore functionality without system reboots:
```bash
# Unbind driver from the crashed hardware node
echo "0000:04:00.3" | sudo tee /sys/bus/pci/drivers/xhci_hcd/unbind

# Assert a hardware reset over the PCIe slot configuration spaces
echo 1 | sudo tee /sys/bus/pci/devices/0000\:04\:00.3/reset

# Rebind driver to re-initialize the root hubs
echo "0000:04:00.3" | sudo tee /sys/bus/pci/drivers/xhci_hcd/bind
```

### 2. Modify Kernel Initial Parameter Options (Permanent Fix)
Adjust kernel translation layouts to remove scheduling latencies:
1. Open boot configurations:
   ```bash
   sudo nano /etc/default/grub
   ```
2. Append `iommu=pt` and `usbcore.autosuspend=-1` to `GRUB_CMDLINE_LINUX_DEFAULT`:
   ```text
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iommu=pt usbcore.autosuspend=-1"
   ```
   * `iommu=pt`: Enables pass-through mode for physical devices, removing IOMMU translation layers.
   * `usbcore.autosuspend=-1`: Hard-disables low-power transitions on the root hub.
3. Commit mutations:
   ```bash
   sudo update-grub
   ```

### 3. Deactivate SEGGER J-Link Emulated Storage Endpoints
To decrease total endpoint allocation on the xHCI scheduler, turn off the unneeded mass storage volumes on the target development chips:
1. Initialize target connection:
   ```bash
   JLinkExe
   ```
2. Disable the interface descriptor inside internal non-volatile memory:
   ```text
   MSDDisable
   ```
3. Cycle target physical power connections.
