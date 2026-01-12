#!/usr/bin/env bash
set -euo pipefail

# Usage: ./run_with_env.sh path/to/script.py [args...]

if [ ! -f .env ]; then
  echo "Missing .env file. Copy .env.example and fill Access_key/Secret_key first." >&2
  exit 1
fi

set -a
source .env
set +a

python3 "$@"