# NVIDIA Driver DKMS Build Failure & Kernel Header Mismatch Resolution

## Environment
* **OS:** Ubuntu 24.04 LTS (Noble Numbat)
* **GPU:** NVIDIA GeForce GTX 1060
* **Symptom:** Display suddenly dropped to standard fallback resolution (stretched screen ratio). `nvidia-smi` failed with:
  `NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`

---

## Root Cause Analysis

The primary failure occurred during kernel module compilation via DKMS following a kernel/package update.

1. **Missing Kernel Build Headers & Tooling:**
   The post-installation script for `linux-modules-nvidia-580-7.0.0-28-generic` failed due to missing binary build dependencies in `/usr/src/linux-headers-7.0.0-28-generic/`:
   * `objtool: not found`
   * `cannot open linker script file /usr/src/linux-headers-7.0.0-28-generic/scripts/module.lds`
   * `sha256sum: nvidia.ko: No such file or directory`

2. **Package Dependency Conflict (Driver Version Collision):**
   A partial upgrade created a lock-state between `nvidia-driver-580` (partially configured/broken) and `nvidia-driver-550` / `nvidia-dkms-550` (blocked by dependency resolution failures).

3. **Fallback Display Server Engagement:**
   Because `nvidia.ko` failed to build and load, the kernel fell back to basic framebuffer software rendering (`llvmpipe`), producing stretched desktop dimensions.

---

## Remediation Protocol

### Step 1: Complete Removal of Broken NVIDIA Packages
Purge all existing NVIDIA driver packages and leftover DKMS modules to clear `dpkg` state:

```bash
sudo apt purge "*nvidia*"
sudo apt autoremove --purge

```

### Step 2: Reinstall Kernel Headers and Build Infrastructure

Ensure `build-essential`, `dkms`, and kernel headers matching the active running kernel are installed and intact:

```bash
sudo apt update
sudo apt install --reinstall build-essential dkms linux-headers-generic linux-headers-$(uname -r)

```

### Step 3: Repair Dpkg Database State

Force resolution of pending package configuration scripts:

```bash
sudo dpkg --configure -a

```

### Step 4: Automated Recommended Driver Installation

Trigger Ubuntu's driver detection utility to pull and compile the optimal driver for GTX 1060:

```bash
sudo ubuntu-drivers install

```

### Step 5: Reboot

Reboot to unload software fallback and initialize the compiled NVIDIA kernel modules:

```bash
sudo reboot

```

---

## Verification

Post-reboot verification:

```bash
# Verify kernel module load state
lsmod | grep nvidia

# Verify driver communications and GPU status
nvidia-smi

```