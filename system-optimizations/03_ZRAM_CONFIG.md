# 03: ZRAM Configuration (Ubuntu/Debian/Mint)

ZRAM creates a compressed swap device directly in RAM. Data is compressed in real-time, avoiding slow disk writes and reducing SSD wear.

## Installation

Install the management utility for compressed swap:

```bash
sudo apt update && sudo apt install zram-tools -y
```

## Parameter Configuration

Configuration is managed via the global defaults file:
**Path**: `/etc/default/zramswap`

Modify or add the following lines to allocate 60% of available RAM for compressed swap using the `zstd` (high-speed) compression algorithm:

```plaintext
ALGO=zstd
PERCENT=60
PRIORITY=100
```

## Application and Validation

1.  **Restart Service**:
    Apply the changes by restarting the zramswap daemon:

    ```bash
    sudo systemctl restart zramswap
    ```

2.  **Verify Activation**:
    Check the status of the compressed device:

    ```bash
    zramctl
    ```

    The output should display the `/dev/zram0` device, the `zstd` algorithm, and a disk size corresponding to 60% of your total RAM.