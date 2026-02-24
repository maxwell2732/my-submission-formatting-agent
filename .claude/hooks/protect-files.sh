#!/bin/bash
# Block accidental edits to protected files
# Customize PROTECTED_PATTERNS below for your project
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=""

# Extract file path based on tool type
if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
fi

# No file path = not a file operation, allow
if [ -z "$FILE" ]; then
  exit 0
fi

# ============================================================
# CUSTOMIZE: Add patterns for files you want to protect
# Uses basename matching — add full paths for more precision
# ============================================================
PROTECTED_PATTERNS=(
  "Bibliography_base.bib"
  "settings.json"
)

# Also protect original manuscripts from accidental modification.
# Check for writes into manuscripts/ directory (full path check).
if [[ "$FILE" == */manuscripts/* ]] && [[ "$FILE" != */manuscripts/.gitkeep ]]; then
  echo "Protected: manuscripts/ is read-only. Work on outputs/ copies instead." >&2
  exit 2
fi

# Protect guidelines/ YAML files from accidental overwrite
# (allow creation of new files, block overwriting existing ones).
if [[ "$FILE" == */guidelines/*.yml ]] && [ -f "$FILE" ]; then
  # File already exists — confirm before overwriting
  echo "Warning: $FILE already exists. Re-running /parse-guidelines will overwrite it." >&2
  # Allow (exit 0) — just warn. User approved via skill invocation.
fi

BASENAME=$(basename "$FILE")
for PATTERN in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$BASENAME" == "$PATTERN" ]]; then
    echo "Protected file: $BASENAME. Edit manually or remove protection in .claude/hooks/protect-files.sh" >&2
    exit 2
  fi
done

exit 0
