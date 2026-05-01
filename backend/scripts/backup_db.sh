#!/usr/bin/env bash
# backup_db.sh – Automated daily backup for PostgreSQL.
# ---------------------------------------------------
# This script creates a timestamped dump of the production database,
# compresses it with gzip, and stores it under /var/backups/postgres.
# It is intended to be run via cron (e.g. 02:00 daily).
# ---------------------------------------------------
set -euo pipefail

# Load environment variables from a .env file located next to this script.
# Required variables: DATABASE_URL, BACKUP_DIR, APP_SECRET_KEY (for pgcrypto).
if [[ -f "$(dirname "$0")/.env" ]]; then
    export $(grep -v '^#' "$(dirname "$0")/.env" | xargs)
fi

# Verify required vars.
: "${DATABASE_URL?Missing DATABASE_URL}"
: "${BACKUP_DIR?Missing BACKUP_DIR}"

# Create backup directory if it does not exist.
mkdir -p "${BACKUP_DIR}"

# Generate filename.
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
FILE="${BACKUP_DIR}/mapgenius_${TIMESTAMP}.sql.gz"

# Use pg_dump with the URL. The URL must be in libpq format.
pg_dump "$DATABASE_URL" --no-owner --no-acl | gzip > "$FILE"

echo "Backup created at $FILE"
