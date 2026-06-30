#!/usr/bin/env bash
set -euo pipefail

echo "=== Loga SMS Python (FastAPI) Integration Sample ==="

# 1. Copy environment if not present
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[INFO] .env created from .env.example — edit it with your credentials"
fi

# 2. Create virtual environment
if [ ! -d .venv ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv .venv
fi

# 3. Activate and install
echo "[INFO] Installing dependencies..."
source .venv/bin/activate
pip install -q -r requirements.txt

# 4. Run the server
echo "[INFO] Starting FastAPI server on http://localhost:8000"
uvicorn main:app --reload --port 8000
