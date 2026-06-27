#!/bin/bash
# DB バックアップ
set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${TIMESTAMP}.sql"

echo ">>> DBバックアップ: ${BACKUP_FILE}"
docker compose exec db pg_dump -U "${POSTGRES_USER:-sunrise_user}" "${POSTGRES_DB:-sunrise_db}" > "${BACKUP_FILE}"
echo ">>> 完了: ${BACKUP_FILE}"
