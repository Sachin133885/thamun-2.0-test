#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo 'Python 3.10+ is required.' >&2; exit 1; }
command -v npm >/dev/null || { echo 'Node.js 22.12+ and npm are required.' >&2; exit 1; }
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install -r api/requirements.txt
fi
if ! .venv/bin/python -c 'import fastapi, lightgbm, sqlalchemy, jwt' >/dev/null 2>&1; then
  .venv/bin/python -m pip install -r api/requirements.txt
fi
if ! .venv/bin/python -c 'import json, pathlib, sklearn; p = pathlib.Path("ml/models/meta.json"); assert p.exists(); assert json.loads(p.read_text())["versions"]["scikit_learn"] == sklearn.__version__; assert all(pathlib.Path("ml/models", f).exists() for f in ("risk.txt", "categorizer.txt", "isolation_forest.pkl"))' >/dev/null 2>&1; then
  .venv/bin/python -m data.generate
  .venv/bin/python -m ml.train
  .venv/bin/python -m ml.evaluate
fi
if [[ ! -d web/node_modules ]]; then
  (cd web && npm ci)
fi
.venv/bin/python -m uvicorn api.main:app --host 127.0.0.1 --port "${API_PORT:-8000}" &
API_PID=$!
cleanup() { kill "$API_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
echo 'Open http://localhost:5173 — Evidence also works at /#evidence without the API.'
cd web
npm run dev -- --host 127.0.0.1
