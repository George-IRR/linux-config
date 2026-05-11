# 07: ModelSim ASE 20.1 Initialization & Scaling

Documentation for resolving 32-bit shared library dependency failures and high-resolution (HiDPI/4K) UI scaling limitations encountered when running Intel FPGA ModelSim 20.1 on modern systems (specifically tested on Ubuntu 26.4).

## Part 1: 32-bit Library Dependencies (Startup Fixes)

ModelSim 20.1 ASE is inherently a 32-bit application. On newer operating systems like Ubuntu 26.4, it will abort startup with "cannot open shared object file" errors (e.g., `libXext.so.6`, `libXft.so.2`) because the 32-bit (`i386`) packages are not present by default. Furthermore, legacy libraries like `libncurses5` have been completely removed from modern package repositories.

### 1. Enable Architecture & Install Core Libraries
Enable the 32-bit architecture layer and install the essential X11 libraries:

```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install libxext6:i386 libxft2:i386 libxrender1:i386 libxtst6:i386 libxi6:i386

```

### 2. The Ncurses Legacy Workaround

Because Ubuntu 26.4 replaced `libncurses5` with version 6, ModelSim will fail to initialize its command shell. The solution is to install the newer 32-bit library and create symbolic links to emulate the missing version 5:

```bash
# Install the modern version 6 library
sudo apt install libncurses6:i386

# Generate symbolic links targeting version 5 expectations
sudo ln -s /usr/lib/i386-linux-gnu/libncurses.so.6 /usr/lib/i386-linux-gnu/libncurses.so.5
sudo ln -s /usr/lib/i386-linux-gnu/libtinfo.so.6 /usr/lib/i386-linux-gnu/libtinfo.so.5

```

## Part 2: HiDPI / 4K UI Scaling Fix

ModelSim utilizes an outdated Tk graphical toolkit that completely ignores modern system-wide display scaling variables. On high-resolution laptops or monitors, the UI elements and icons render at a 1:1 pixel mapping, resulting in an unreadably small interface. Tweaking internal font preferences is insufficient, as the application's bitmap icons remain static.

### Implementation: Nested Compositor (Weston)

The most robust solution is to isolate the application within a nested display compositor (`weston`) configured to execute a forced, pixel-level hardware scale.

1. **Install Dependencies:**
```bash
sudo apt install weston

```


2. **Execution Protocol:**
Launch an isolated desktop window scaled to 200% (`--scale=2`):
```bash
weston --xwayland --scale=2

```


3. **Launch Application:**
* Open the native terminal from the top-left menu *inside* the new Weston window.
* Execute the application binary from within this nested environment:


```bash
cd ~/intelFPGA/20.1/modelsim_ase/linux
./vsim

```



This approach intercepts the X11 rendering and magnifies the entire application instance, scaling both text and hardcoded bitmap icons proportionally without fragmenting the UI layout.

