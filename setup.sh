#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
python -c "from app.services.database import init_db; init_db(); print('Database initialized.')"
echo "Setup complete. Run: source .venv/bin/activate && ./run.sh"
