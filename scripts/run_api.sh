#!/usr/bin/env bash
set -euo pipefail
source venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload