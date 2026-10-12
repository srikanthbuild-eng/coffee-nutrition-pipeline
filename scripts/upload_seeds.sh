#!/usr/bin/env bash
# Uploads every seed CSV into the landing volume, in a folder named after today's date:
#   /Volumes/<catalog>/bronze/landing/seed/load_date=YYYY-MM-DD/<file>.csv
#
# Usage (from the project root):
#   ./scripts/upload_seeds.sh             # catalog = workspace
#   ./scripts/upload_seeds.sh my_catalog  # any other catalog
set -euo pipefail

CATALOG="${1:-workspace}"
LOAD_DATE="$(date +%F)"
DEST="dbfs:/Volumes/${CATALOG}/bronze/landing/seed/load_date=${LOAD_DATE}"

echo "Uploading seed_data/*.csv to ${DEST}"
databricks fs mkdir "${DEST}"

for file in seed_data/*.csv; do
  databricks fs cp "${file}" "${DEST}/$(basename "${file}")" --overwrite
  echo "  uploaded $(basename "${file}")"
done

echo
echo "Files now in the volume:"
databricks fs ls "${DEST}"
