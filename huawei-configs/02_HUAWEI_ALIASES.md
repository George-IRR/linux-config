# 02: Shell Aliases for Battery Control

Manual threshold adjustment profiles defined for interactive use.

## Configuration

Inject the following logic into the shell environment via `~/.bashrc`.

```bash
# Huawei Battery Threshold Profiles
# Preservation Mode (40-70%)
alias bat-home='echo "40 70" | sudo tee /sys/devices/platform/huawei-wmi/charge_control_thresholds'

# Balanced Mode (70-90%)
alias bat-office='echo "70 90" | sudo tee /sys/devices/platform/huawei-wmi/charge_control_thresholds'

# Maximum Capacity (95-100%)
alias bat-full='echo "95 100" | sudo tee /sys/devices/platform/huawei-wmi/charge_control_thresholds'
```

## Application

1.  Append code block to `~/.bashrc`.
2.  Refresh shell: `source ~/.bashrc`.
3.  Execute `bat-home`, `bat-office`, or `bat-full` as needed.