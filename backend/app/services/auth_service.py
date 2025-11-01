# D:\SmartApc\backend\app\services\auth_service.py
import re
import hashlib
from datetime import datetime, timedelta
from app.repositories.auth_repo import (
    id_exists,
    email_exists,
    phone_exists,
    insert_auth_code,
    get_valid_auth_code,
    mark_code_used,
    create_user,
    get_user_by_id,   # 로그인용
)
from app.helpers.sql_exec import get_connection  # ← 절대경로로

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^\d{9,15}$")
ID_RE    = re.compile(r"^[a-zA-Z0-9_\-\.]{4,32}$")

def _hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _clean_phone(p: str) -> str:
    return re.sub(r"[^0-9]", "", p or "")

def verify_base_service(payload: dict):
    us_id    = (payload.get("us_id") or "").strip()
    us_name  = (payload.get("us_name") or "").strip()
    us_email = (payload.get("us_email") or "").strip().lower()
    us_phone = _clean_phone(payload.get("us_phone"))

    if not us_name or len(us_name) < 2:
        return False, {"ok": False, "reason": "invalid_name"}
    if us_email and not EMAIL_RE.match(us_email):
        return False, {"ok": False, "reason": "invalid_email_format"}
    if us_phone and not PHONE_RE.match(us_phone):
        return False, {"ok": False, "reason": "invalid_phone_format"}
    if not (us_email or us_phone):
        return False, {"ok": False, "reason": "need_email_or_phone"}

    if us_id:
        if not ID_RE.match(us_id):
            return False, {"ok": False, "reason": "invalid_id_format"}
        with get_connection() as conn:
            if id_exists(conn, us_id):
                return False, {"ok": False, "reason": "id_exists"}
    return True, {"ok": True}

def send_code_service(payload: dict):
    channel = (payload.get("channel") or "email").lower()
    target  = (payload.get("target") or "").strip()
    if channel not in ("email", "sms"):
        return False, {"ok": False, "reason": "invalid_channel"}
    if channel == "email":
        if not EMAIL_RE.match(target):
            return False, {"ok": False, "reason": "invalid_email_format"}
    else:
        target = _clean_phone(target)
        if not PHONE_RE.match(target):
            return False, {"ok": False, "reason": "invalid_phone_format"}

    code = f"{datetime.utcnow().microsecond % 1000000:06d}"
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    with get_connection() as conn:
        insert_auth_code(conn, channel, target, code, expires_at)
    return True, {"ok": True, "dev_code": code, "expires_in_sec": 300}

def check_code_service(payload: dict):
    channel = (payload.get("channel") or "email").lower()
    target  = (payload.get("target") or "").strip()
    code    = (payload.get("code") or "").strip()
    if channel not in ("email", "sms"):
        return False, {"ok": False, "reason": "invalid_channel"}
    if channel == "email":
        if not EMAIL_RE.match(target):
            return False, {"ok": False, "reason": "invalid_email_format"}
    else:
        target = _clean_phone(target)
        if not PHONE_RE.match(target):
            return False, {"ok": False, "reason": "invalid_phone_format"}

    with get_connection() as conn:
        row = get_valid_auth_code(conn, channel, target, code)
        if not row:
            return False, {"ok": False, "reason": "invalid_or_expired_code"}
        mark_code_used(conn, row["ac_id"])
    return True, {"ok": True}

def check_id_service(payload: dict):
    us_id = (payload.get("us_id") or payload.get("id") or "").strip()
    if not ID_RE.match(us_id):
        return False, {"ok": False, "reason": "invalid_id_format"}
    with get_connection() as conn:
        exists = id_exists(conn, us_id)
    return True, {"ok": True, "exists": bool(exists)}

def register_member_service(payload: dict):
    us_id    = (payload.get("us_id") or "").strip()
    us_pass  = (payload.get("us_pass") or "").strip()
    us_name  = (payload.get("us_name") or "").strip()
    us_email = (payload.get("us_email") or "").strip().lower()
    us_phone = _clean_phone(payload.get("us_phone"))
    us_role  = (payload.get("us_role") or "member").strip()

    if not (us_id and us_pass and us_name):
        return False, {"ok": False, "reason": "missing_fields"}
    if not ID_RE.match(us_id):
        return False, {"ok": False, "reason": "invalid_id_format"}
    if us_email and not EMAIL_RE.match(us_email):
        return False, {"ok": False, "reason": "invalid_email_format"}
    if us_phone and not PHONE_RE.match(us_phone):
        return False, {"ok": False, "reason": "invalid_phone_format"}

    with get_connection() as conn:
        if id_exists(conn, us_id):
            return False, {"ok": False, "reason": "id_exists"}
        if us_email and email_exists(conn, us_email):
            return False, {"ok": False, "reason": "email_exists"}
        if us_phone and phone_exists(conn, us_phone):
            return False, {"ok": False, "reason": "phone_exists"}

        hashed = hashlib.sha256(us_pass.encode("utf-8")).hexdigest()
        us_no = create_user(conn, us_id, hashed, us_name, us_email, us_phone, us_role)
    return True, {"ok": True, "us_no": us_no}

def login_service(payload: dict):
    us_id   = (payload.get("id") or payload.get("us_id") or "").strip()
    us_pass = (payload.get("password") or payload.get("us_pass") or "").strip()
    if not us_id or not us_pass:
        return False, {"reason": "MISSING_CREDENTIALS"}
    with get_connection() as conn:
        user = get_user_by_id(conn, us_id)
        if not user:
            return False, {"reason": "INVALID_USER"}
        if user["us_pass"] != hashlib.sha256(us_pass.encode("utf-8")).hexdigest():
            return False, {"reason": "INVALID_PASSWORD"}
        public_user = {"id": user["us_id"], "name": user["us_name"], "roles": [user.get("us_role") or "member"]}
        return True, {"user": public_user}

def get_session_user_service(sess_user):
    if not isinstance(sess_user, dict):
        return None
    if not all(k in sess_user for k in ("id", "name", "roles")):
        return None
    return sess_user
