#!/usr/bin/env sh
set -eu

echo "Waiting for database..."
python - <<'PY'
import time
from sqlalchemy import create_engine, text

from app.config import settings

url = settings.database_url_sync
deadline = time.time() + 60
last_err = None

while time.time() < deadline:
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database is ready.")
        break
    except Exception as e:
        last_err = e
        time.sleep(1)
else:
    raise SystemExit(f"Database did not become ready in time: {last_err!r}")
PY

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"

