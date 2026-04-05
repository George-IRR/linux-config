# 01: Huawei Battery Threshold Automation

Documentation for overriding kernel-level charging behavior at system startup.

## Implementation: Systemd Service

The `battery-threshold.service` ensures the "Home" profile (40%-70%) is applied before user login.

**File Path**: `/etc/systemd/system/battery-threshold.service`

```ini
[Unit]
Description=Set Huawei battery charge thresholds at boot
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo "40 70" > /sys/devices/platform/huawei-wmi/charge_control_thresholds'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

## Operations

1.  **Initialize**: `sudo systemctl daemon-reload`
2.  **Enable**: `sudo systemctl enable battery-threshold.service`
3.  **Execute**: `sudo systemctl start battery-threshold.service`
4.  **Verify**: `cat /sys/devices/platform/huawei-wmi/charge_control_thresholds`
