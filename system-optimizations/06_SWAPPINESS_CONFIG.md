# 06: Swappiness Optimization

This document describes the configuration of the `vm.swappiness` parameter to optimize how the system utilizes RAM and to protect the integrity of the SSD.

## Verifying the Current Value

By default, Ubuntu typically uses a value of `60`. This means the system will start moving data from RAM to swap relatively early. To check your current value, run:

```bash
cat /proc/sys/vm/swappiness
```

## Modifying the Parameter

To reduce the aggressiveness of swap usage, the value has been set to `10`. This change forces the Linux kernel to prefer using physical RAM until it is nearly full.

### Steps for Permanent Application:

1.  Edit the system configuration file:
    ```bash
    sudo nano /etc/sysctl.conf
    ```
2.  Add the following line to the end of the file:
    ```plaintext
    vm.swappiness=10
    ```
3.  Apply the change immediately without a reboot:
    ```bash
    sudo sysctl -p
    ```

## Why Apply This Optimization?

Setting `vm.swappiness=10` provides several direct benefits to system performance:

* **Reduced SSD Wear**: By limiting how frequently the system writes temporary data to the swap partition on the disk, you reduce unnecessary write cycles, extending the lifespan of the SSD.
* **Improved Latency**: RAM is significantly faster than any SSD. Keeping applications in RAM for longer makes the system more responsive and prevents "hiccups" when switching between windows.
* **Synergy with ZRAM**: Since ZRAM is already configured to provide compressed swap within RAM, a lower swappiness value ensures the system uses actual physical RAM as efficiently as possible before resorting to any form of swap.