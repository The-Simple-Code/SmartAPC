# D:\SmartApc\backend\app\routes\auth_routes.py
from flask import Blueprint, request, jsonify, session
from app.services.auth_service import (
    verify_base_service,
    send_code_service,
    check_code_service,
    check_id_service,
    register_member_service,
    login_service,
    get_session_user_service,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/verify_base")
def verify_base():
    payload = request.get_json(silent=True) or {}
    ok, data = verify_base_service(payload)
    return jsonify(data), (200 if ok else 400)

@auth_bp.post("/send_code")
def send_code():
    payload = request.get_json(silent=True) or {}
    ok, data = send_code_service(payload)
    return jsonify(data), (200 if ok else 400)

@auth_bp.post("/check_code")
def check_code():
    payload = request.get_json(silent=True) or {}
    ok, data = check_code_service(payload)
    return jsonify(data), (200 if ok else 400)

@auth_bp.route("/check_id", methods=["GET","POST"])
def check_id():
    payload = {"us_id": request.args.get("us_id") or request.args.get("id")} if request.method=="GET" else (request.get_json(silent=True) or {})
    ok, data = check_id_service(payload)
    return jsonify(data), (200 if ok else 400)

@auth_bp.post("/register_member")
def register_member():
    payload = request.get_json(silent=True) or {}
    ok, data = register_member_service(payload)
    return jsonify(data), (200 if ok else 400)

@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    ok, data = login_service(payload)
    if ok:
        session["user"] = data["user"]  # 세션에 최소 정보 저장
        return jsonify({"ok": True, "user": data["user"]}), 200
    return jsonify({"ok": False, "error": data.get("reason","LOGIN_FAILED")}), 401

@auth_bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True}), 200

@auth_bp.get("/me")
def me():
    user = get_session_user_service(session.get("user"))
    return (jsonify({"ok": True, "user": user}), 200) if user else (jsonify({"ok": False}), 200)
