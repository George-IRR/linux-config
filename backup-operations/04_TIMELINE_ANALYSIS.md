# 04: Timestamp & Timeline Analysis

Techniques for filtering files and backups using strict chronological parameters with `zpaqfranz`.

## Filtering by Date Range
To locate files modified strictly within a specific timeframe, utilize the `-datefrom` and `-dateto` parameters. Supported formats include `YYYY`, `YYYYMM`, `YYYY-MM-DD`, or `YYYY-MM-DD_HH:MM:SS`.

```bash
# Find all files modified between January 1st and May 1st
zpaqfranz find /opt/containers/app_data/ -datefrom 20240101 -dateto 2024-05-01
```

## Analyzing File Age
The `dir` command acts as a heavily upgraded system listing tool. It can be used to audit aging files or track recent modifications.

```bash
# Show files older than 30 days, sorted by date (/od)
zpaqfranz dir /opt/containers/app_data/ /s /age+30 /od

# Show files newer than 7 days, sorted by newest first (/o-d)
zpaqfranz dir /opt/containers/app_data/ /s /age-7 /o-d
```

## Inspecting Internal Archive Timestamps
To view the specific creation dates of files stored *inside* the archive (rather than just the backup execution date), append the `-date` flag to the list command. Append `-utc` to normalize times across different server timezones.

```bash
zpaqfranz l "/mnt/backups/app_data_???????.zpaq" -date -utc -key "SuperSecretPassword"
```
