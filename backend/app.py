# D:\SmartAPC\backend\app.py
from flask import Flask, session, jsonify
from flask_cors import CORS
from datetime import timedelta
import os

def create_app():
    app = Flask(__name__)

    # --- 세션/쿠키 기본 ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
    # JSON 한글 깨짐 방지
    app.config["JSON_AS_ASCII"] = False

    # === 쿠키 전략 ===
    # ① 추천(개발): 프론트가 Vite 프록시를 사용해 '/api'로 호출하면 "같은 오리진" 처럼 동작 → Lax로 충분
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False  # http 개발 환경

    # 만약 프론트가 프록시 없이 http://211.42.144.32:5173 → http://127.0.0.1:5000 직접 호출이라면
    # 교차 오리진 쿠키가 필요 → 아래처럼 바꿔야 하지만, 'Secure=True'는 HTTPS 필수!
    # app.config["SESSION_COOKIE_SAMESITE"] = "None"
    # app.config["SESSION_COOKIE_SECURE"] = True  # ← 이 경우 서버를 HTTPS로 띄워야 함

    # --- CORS: 개발 오리진 열기 ---
    allowed = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://211.42.144.32:5173",
        "http://192.168.0.115:5173",
    ]
    CORS(
        app,
        supports_credentials=True,
        resources={r"/api/*": {"origins": allowed}},
    )

    # --- 블루프린트 등록 ---
    from app.routes import register_blueprints
    register_blueprints(app)

    # --- 헬스체크 ---
    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "auth": bool(session.get("user"))})

    return app

if __name__ == "__main__":
    app = create_app()
    # 개발 모드: 자동 리로드 & 상세 로그
    app.run(host="0.0.0.0", port=5000, debug=True)
