#!/usr/bin/env bash
set -euo pipefail

python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cp -n .env.example .env || true
echo "✅ Setup complete. Edit .env with your Neo4j creds and HF token."