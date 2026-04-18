#!/usr/bin/env bash

# ------------------------------------------------------------
# Safely move a file into a quarantine directory to test whether
# it is still required by the system (e.g., flagged libraries).
#
# Usage:
#   ./quarantine_file.sh <target_file> [quarantine_dir] [dry_run]
#
# Examples:
#   ./quarantine_file.sh /opt/lib123
#   ./quarantine_file.sh /opt/lib123 /opt/quarantine
#   ./quarantine_file.sh /opt/lib123 /opt/quarantine true
#
# Arguments:
#   target_file      (required) Full path to the file you want to quarantine
#   quarantine_dir   (optional) Where the file will be moved (default: ./quarantine)
#   dry_run          (optional) If "true", shows what would happen without making changes
#
# Notes:
# - Run with sudo if required for file permissions
# - Always verify application behavior after moving the file
# - Use the rollback command if issues occur
# ------------------------------------------------------------

set -u # Treats unset variables as an error

TARGET_FILE="$1"
QUARANTINE_DIR="${2:-./quarantine}"
DRY_RUN="${3:-false}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

# Validate input
if [ -z "$TARGET_FILE" ]; then
  echo "Usage: $0 <target_file> [quarantine_dir] [dry_run]"
  exit 1
fi

# Does the file exists
if [ ! -f "$TARGET_FILE" ]; then
  echo "Target file not found: $TARGET_FILE"
  exit 1
fi

# Create quarantine directory if needed
mkdir -p "$QUARANTINE_DIR"

# Build destination
BASENAME="$(basename "$TARGET_FILE")"
QUARANTINED_FILE="${QUARANTINE_DIR}/${TIMESTAMP}_${BASENAME}"

# Dry run mode if enabled
if [ "$DRY_RUN" = "true" ]; then
  echo "[DRY RUN] Would move:"
  echo "  From: $TARGET_FILE"
  echo "  To:   $QUARANTINED_FILE"
  exit 0
fi

# Moving the file
mv "$TARGET_FILE" "$QUARANTINED_FILE"

# Output
echo "File quarantined successfully"
echo "Original: $TARGET_FILE"
echo "Quarantined: $QUARANTINED_FILE"
echo
echo "Rollback command:"
echo "mv \"$QUARANTINED_FILE\" \"$(dirname "$TARGET_FILE")/$BASENAME\""