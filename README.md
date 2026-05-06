# Linux Operations Manual

A technical record of system modifications and hardware-specific configurations for Ubuntu. This repository serves as the definitive guide for environment reproduction.

## Table of Contents

### Hardware Optimizations

  * [01: Huawei Battery Threshold Automation](./huawei-configs/01_HUAWEI_BATTERY_SYSTEMD.md)
      * Direct systemd integration for boot-time power management.
  * [02: Shell Aliases for Battery Control](./huawei-configs/02_HUAWEI_ALIASES.md)
      * Interactive commands for real-time profile switching.

### Performance Optimizations

  * [03: ZRAM Configuration](./system-optimizations/03_ZRAM_CONFIG.md)
      * Implementation of compressed RAM swap to eliminate slow disk writes.
  * [04: Rclone VFS Mount Configuration](./system-optimizations/04_RCLONE_VFS_MOUNT.md)
      * Systemd integration for high-performance cloud storage mounting with optimized metadata caching.
  * [06: Swappiness Optimization](./system-optimizations/06_SWAPPINESS_CONFIG.md)
      * Reducing disk write frequency to extend SSD lifespan and improve responsiveness.
      
### System Administration

  * [05: Systemd Service Management](./system-administration/05_SYSTEMD_MANAGEMENT.md)
      * Essential commands for monitoring, restarting, and troubleshooting background services.

### Software Management

  * [07: Flatpak Setup](./software-management/07_FLATPAK_SETUP.md)
      * Containerized application isolation, repository installation, and command alias mapping.
  * [08: Java Memory Allocation](./software-management/08_JAVA_MEMORY.md)
      * Heap memory limit configuration for `.jar` executables.
  * [09: AppImageLauncher Configuration](./software-management/09_APPIMAGE_LAUNCHER.md)
      * System integration protocol for portable `.AppImage` execution.
  * [10: Docker Engine Configuration](./software-management/10_DOCKER_ENGINE.md)
      * Official repository integration, installation, and socket permission management.
  * [11: Docker Management Interfaces](./software-management/11_DOCKER_INTERFACES.md)
      * Deployment of Portainer (Web UI) and Lazydocker (TUI) for container orchestration.

### Backup & Disaster Recovery
  * [12: Hardened Multipart Backup Configurations](./backup-operations/12_HARDENED_MULTIPART.md)
      * Implementation of chunked, encrypted, and deduplicated archives with fail-safe mechanisms for container data.
  * [13: Data Restoration & Time Travel](./backup-operations/13_RESTORATION_PROTOCOLS.md)
      * Protocols for extracting metadata-accurate files and executing point-in-time rollbacks.
  * [14: Archive Integrity Verification](./backup-operations/14_INTEGRITY_VERIFICATION.md)
      * Deep-scanning methodologies for multipart archives and pre-backup size estimations.
  * [15: Timestamp & Timeline Analysis](./backup-operations/15_TIMELINE_ANALYSIS.md)
      * Advanced querying techniques for auditing file ages and finding specific archive versions across time.
  * [16: Automated Backup Scheduling](./backup-operations/16_BACKUP_AUTOMATION.md)`
      * Systemd timer and service configurations for hands-free, scheduled container archiving and automated journal logging.