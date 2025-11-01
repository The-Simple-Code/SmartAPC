# D:\SmartApc\backend\app\__init__.py
from flask import Flask, jsonify, session
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv

import os

load_dotenv()

def _parse_allowed_origins():
    """
    CORS_ALLOW_ORIGINS=콤마구분… (예: http://127.0.0.1:5173,http://211.42.144.32:5173)
    미설정 시 로컬/LAN 기본값 사용.
    """
    raw = os.getenv("CORS_ALLOW_ORIGINS", "").strip()
    if raw:
        return [o.strip() for o in raw.split(",") if o.strip()]
    return [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://192.168.0.115:5173",
        "http://211.42.144.32:5173",
    ]

def create_app(config_name: str = "development"):
    app = Flask(__name__)

    # ✅ 세션/쿠키 (개발)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"   # Vite 프록시(/api) 경유 시 OK
    app.config["SESSION_COOKIE_SECURE"] = False     # http 개발
    app.config["JSON_AS_ASCII"] = False

    # ✅ CORS: /api/* 만 허용 + 쿠키 포함
    allowed = _parse_allowed_origins()
    CORS(
        app,
        supports_credentials=True,   # ← 최상위에 둬야 적용됨
        resources={
            r"/api/*": {
                "origins": allowed,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Disposition"],
            }
        },
    )

    # === 블루프린트 등록 ===
    from app.routes import register_blueprints
    register_blueprints(app)

    # === 간단한 상태 확인 ===
    @app.get("/")
    def root():
        return jsonify(status="ok", service="SmartApc backend", docs="/api/health/app")

    @app.get("/api/ping")
    def ping():
        return jsonify(
            status="ok",
            message="SmartApc backend is running",
            authed=bool(session.get("user")),
        )

    return app
