# Linux Operations Manual

A technical record of system modifications and hardware-specific configurations for Ubuntu. This repository serves as the definitive guide for environment reproduction.

## Table of Contents

### Hardware Optimizations

  * [01: Huawei Battery Threshold Automation](./huawei-configs/01_HUAWEI_BATTERY_SYSTEMD.md)
      * Direct systemd integration for boot-time power management.
  * [02: Shell Aliases for Battery Control](./huawei-configs/02_HUAWEI_ALIASES.md)
      * Interactive commands for real-time profile switching.

### Performance Optimizations

  * [01: ZRAM Configuration](./system-optimizations/01_ZRAM_CONFIG.md)
      * Implementation of compressed RAM swap to eliminate slow disk writes.
  * [02: Rclone VFS Mount Configuration](./system-optimizations/02_RCLONE_VFS_MOUNT.md)
      * Systemd integration for high-performance cloud storage mounting with optimized metadata caching.
  * [03: Swappiness Optimization](./system-optimizations/03_SWAPPINESS_CONFIG.md)
      * Reducing disk write frequency to extend SSD lifespan and improve responsiveness.
  * [04: PipeWire Audio Buffer Optimization](./system-optimizations/04_PIPEWIRE_BUFFER_FIX.md)
      * Persistent configuration override to stabilize audio quantum limits and eliminate lag.
  * [05: AMD Renoir xHCI USB Controller Fix](./system-optimizations/05_AMD_RENOIR_USB_FIX.md)
      * Mitigating kernel crashes and root hub lockups under multi-endpoint load.

### System Administration

  * [01: Systemd Service Management](./system-administration/01_SYSTEMD_MANAGEMENT.md)
      * Essential commands for monitoring, restarting, and troubleshooting background services.
  * [02: Taskbar Performance Monitoring](./system-administration/02_TASKBAR_MONITORING.md)
      * GUI-based integration for real-time CPU, RAM, and Network stats in the system taskbar.

### Server Infrastructure & Management

  * [01: Active and Isolated Network Discovery](./server-management/01_SERVER_DISCOVERY.md)
      * Methodologies for tracing target hardware over live subnets and unmanaged non-DHCP switch environments.
  * [02: iRMC Interface Access & Legacy Cipher Troubleshooting](./server-management/02_IRMC_TROUBLESHOOTING.md)
      * Bypassing modern router intercept vectors and tuning client-side TLS baselines for iRMC S2 chips.
  * [03: Hardened SSH Infrastructure](./server-management/03_HARDENED_SSH_ACCESS.md)
      * Transition protocols for asymmetric cryptographic validation, client alias profiles, and localized network firewalls.

### Hardware Diagnostics & Recovery

  * [01: POST Fault Analysis and Power Subsystem Mapping](./hardware-diagnostics/01_POST_FAULT_ANALYSIS.md)
      * Decoupling critical POST code 0x28, memory subsystem isolation, and tracking power supply thermal cascading events.

### Software Management

  * [01: Flatpak Setup](./software-management/01_FLATPAK_SETUP.md)
      * Containerized application isolation, repository installation, and command alias mapping.
  * [02: Java Memory Allocation](./software-management/02_JAVA_MEMORY.md)
      * Heap memory limit configuration for `.jar` executables.
  * [03: AppImageLauncher Configuration](./software-management/03_APPIMAGE_LAUNCHER.md)
      * System integration protocol for portable `.AppImage` execution.
  * [04: Docker Engine Configuration](./software-management/04_DOCKER_ENGINE.md)
      * Official repository integration, installation, and socket permission management.
  * [05: Docker Management Interfaces](./software-management/05_DOCKER_INTERFACES.md)
      * Deployment of Portainer (Web UI) and Lazydocker (TUI) for container orchestration.
  * [06: Essential Utility Library](./software-management/06_USEFUL_APPS.md)
      * Collection of standard productivity and development tools installed via apt.
  * [07: ModelSim ASE 20.1 Initialization & Scaling](./software-management/07_MODELSIM_UBUNTU_26.md)
      * Resolution for 32-bit shared library dependency failures and HiDPI/4K UI scaling using a nested Weston compositor.

### Backup & Disaster Recovery
  * [01: Hardened Multipart Backup Configurations](./backup-operations/01_HARDENED_MULTIPART.md)
      * Implementation of chunked, encrypted, and deduplicated archives with fail-safe mechanisms for container data.
  * [02: Data Restoration & Time Travel](./backup-operations/02_RESTORATION_PROTOCOLS.md)
      * Protocols for extracting metadata-accurate files and executing point-in-time rollbacks.
  * [03: Archive Integrity Verification](./backup-operations/03_INTEGRITY_VERIFICATION.md)
      * Deep-scanning methodologies for multipart archives and pre-backup size estimations.
  * [04: Timestamp & Timeline Analysis](./backup-operations/04_TIMELINE_ANALYSIS.md)
      * Advanced querying techniques for auditing file ages and finding specific archive versions across time.
  * [05: Automated Backup Scheduling](./backup-operations/05_BACKUP_AUTOMATION.md)
      * Systemd timer and service configurations for hands-free, scheduled container archiving and automated journal logging.
  * [06: Immich Container Backup via Vorta](./backup-operations/06_IMMICH_VORTA_BACKUP.md)
      * Automated database dumping and source selection for containerized photo library preservation.