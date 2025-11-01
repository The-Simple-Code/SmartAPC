# D:\SmartApc\backend\app\routes\health.py
from flask import Blueprint, jsonify
import os, sys

from sqlalchemy import create_engine, text

bp = Blueprint("health", __name__, url_prefix="/api/health")


@bp.get("/app")
def app_health():
    info = { "python": sys.version.split()[0], "flask_env": os.getenv("FLASK_ENV", "unknown"),
             "has_database_url": bool(os.getenv("DATABASE_URL")) }
    return jsonify(status="ok", app=info)

@bp.get("/db")
def db_health():
    url = os.getenv("DATABASE_URL")
    if not url:
        return jsonify(status="error", error="DATABASE_URL not set"), 500
    try:
        engine = create_engine(url, pool_pre_ping=True, future=True)
        with engine.connect() as conn:
            ver = conn.execute(text("SELECT @@VERSION")).scalar()
            probe = conn.execute(text("SELECT 1")).scalar()
        return jsonify(status="ok", probe=probe, version=ver)
    except Exception as e:
        return jsonify(status="error", error=str(e)), 500