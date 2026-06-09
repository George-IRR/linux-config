# 06: Immich Container Backup via Vorta

Documentation for backing up an Immich container deployment using Vorta, leveraging pre-backup database serialization to circumvent file permission blocks and eliminate runtime database corruption.

## Pre-Backup Execution

To prevent Vorta from encountering permission failures on live PostgreSQL database directories and to ensure transactional consistency, the database must be dumped prior to archive initialization.

In Vorta, enter the following statement under **Profiles** → **Misc** → **Pre-backup command**:

```bash
docker exec -e PGPASSWORD="<DB_PASSWORD>" <DATABASE_CONTAINER_NAME> pg_dump -U <DB_USERNAME> <DB_DATABASE_NAME> > /home/<USERNAME>/Docker/immich-app/immich_db_backup.sql

```

*Note: Replace `<DATABASE_CONTAINER_NAME>`, `<DB_PASSWORD>`, `<DB_USERNAME>`, `<DB_DATABASE_NAME>`, and `<USERNAME>` with system-specific environment variables.*

## Vorta Source Selection

Configure the **Sources** tab within the Vorta interface to target only the serialized assets and flat files:

1. **Include**: `/home/<USERNAME>/Docker/immich-app/library` (Target directory for uploaded assets).
2. **Include**: `/home/<USERNAME>/Docker/immich-app/immich_db_backup.sql` (The generated database snapshot).
3. **Exclude**: `/home/<USERNAME>/Docker/immich-app/postgres` (Omit the raw runtime database binary folder to prevent permission blocks).

## Post-Backup Cleanup

To purge unencrypted database dump files remaining on local storage post-archive execution, enter the following statement under **Profiles** → **Misc** → **Post-backup command**:

```bash
rm -f /home/<USERNAME>/Docker/immich-app/immich_db_backup.sql

```
