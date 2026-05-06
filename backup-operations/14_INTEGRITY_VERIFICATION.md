# 14: Archive Integrity Verification

Protocols for ensuring data health outside of the standard backup routine. Highly recommended for automated monthly cronjobs.

## Multipart Deep Scan (`testbackup`)
While the `-test` flag checks data immediately after creation, storage drives can silently corrupt data over time. This reads the master index and mathematically verifies every historical chunk.

```bash
# -verify forces a re-read from the filesystem
# -ssd enables multithreaded processing (do not use on spinning HDDs)
zpaqfranz testbackup "/mnt/backups/app_data_???????.zpaq" -verify -ssd -key "SuperSecretPassword"
```

## Pre-Flight Size Estimation (`sync`)
To estimate how much new or changed data will be compressed *before* committing CPU resources to a backup operation, compare the live directory against the existing archive.

```bash
zpaqfranz sync "/mnt/backups/app_data_???????.zpaq" /opt/containers/app_data/ -ssd
```

## Cross-Directory Hash Validation (`c`)
Used to prove that a copied or restored directory is mathematically identical to the master directory, completely ignoring filenames.

```bash
# -checksum upgrades the check from basic size/name to full file hashing
# -xxh3 dictates the fast hashing algorithm to use
zpaqfranz c /opt/containers/master_data/ /mnt/external_drive/cloned_data/ -checksum -xxh3 -ssd
```