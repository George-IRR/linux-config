# 07: Flatpak Setup

System for installing and managing containerized applications. Eliminates dependency conflicts through application isolation (sandboxing).

## Installation and Configuration

1. Install package:
   ```bash
   sudo apt install flatpak
   ```
2. Add Flathub repository:
   ```bash
   flatpak remote-add --if-not-exists flathub [https://dl.flathub.org/repo/flathub.flatpakrepo](https://dl.flathub.org/repo/flathub.flatpakrepo)
   ```
3. Restart system to apply desktop environment integration.

## Execution Optimization (Aliases)

Default execution requires the full identifier (e.g., `flatpak run com.domain.app`).
Inject aliases into `~/.bashrc` for brevity.

1. Edit configuration:
   ```bash
   nano ~/.bashrc
   ```
2. Add syntax for shortcut mapping:
   ```bash
   alias short_name='flatpak run com.domain.app'
   ```
3. Reload shell:
   ```bash
   source ~/.bashrc
   ```