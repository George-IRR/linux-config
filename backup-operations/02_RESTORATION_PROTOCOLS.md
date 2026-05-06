# 02: Data Restoration & Time Travel

Because `zpaqfranz` backups are immutable and incremental by default, the archive contains the entire history of the data. These commands handle standard extraction and historical rollbacks.

## Standard Extraction
Extract the archive back to a target directory. You **must** include `-tar` to ensure metadata (like Unix user ownership) saved during the backup phase is applied.
```bash
zpaqfranz x "/mnt/backups/app_data_???????.zpaq" -to "/opt/containers/app_data_restored/" -tar -key "SuperSecretPassword"
```

## Time Travel (Rollback)
If live data is corrupted prior to the latest backup run, the most recent archive version contains the corruption. Use `-until` to roll back to a clean state.

1.  **Identify the Target Version:**
    List all versions stored in the archive to find the correct rollback point:
    ```bash
    zpaqfranz i "/mnt/backups/app_data_???????.zpaq" -key "SuperSecretPassword"
    ```

2.  **Execute the Rollback:**
    Extract exactly how the folder looked at a specific version (e.g., Version `5`):
    ```bash
    zpaqfranz x "/mnt/backups/app_data_???????.zpaq" -to "/opt/containers/app_data_restored/" -until 5 -tar -key "SuperSecretPassword"
    
```