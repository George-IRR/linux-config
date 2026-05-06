# 12: Hardened Multipart Backup Configurations

Documentation for creating highly compressed, chunked backups optimized for disaster recovery and safe cloud synchronization using `zpaqfranz`.

## Execution Parameters (The "Fail-Safe" Flags)
When backing up critical application data (especially container bind-mounts), the standard backup command must be fortified:

* `-m5`: Applies maximum compression (use `-m2` for lower CPU overhead).
* `-tar`: **Critical.** Preserves POSIX metadata, ensuring exact Unix user/group ownership and execution permissions are retained.
* `-checksize <size>`: Safety lock. Aborts if the destination drive lacks the specified free space.
* `-tmp`: Writes the active backup as a `.tmp` file. It is only renamed to `.zpaq` upon completion, preventing cloud-syncing tools from uploading half-finished chunks.
* `-test`: Triggers an immediate post-write integrity verification against the filesystem.
* `-backupxxh3`: Upgrades the standard chunk verification hash to XXH3 for faster, stronger cryptographic confidence.
* `-filelist`: Generates a lightweight text index of all backed-up files inside the archive.
* `-index <path>`: Extracts the master archive map (index) and `.pid` files into a separate directory.
* `-key <password>`: Applies AES-256 encryption.

## Implementation

Execute the following to create a scalable, multi-part archive (using `???????` to allow scaling up to millions of chunks without naming conflicts).
```bash
zpaqfranz backup "/mnt/backups/app_data_???????.zpaq" /opt/containers/app_data/ \
  -index "/mnt/backups/index_maps/" \
  -m5 \
  -tar \
  -checksize 10g \
  -key "SuperSecretPassword" \
  -tmp \
  -test \
  -backupxxh3 \
  -filelist \
  -not "*/cache/*" -not "*/tmp/*"
```