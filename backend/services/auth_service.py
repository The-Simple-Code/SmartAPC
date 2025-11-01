# D:\SmartAPC\backend\services\auth_service.py
import re
import hashlib
from datetime import datetime, timedelta
from repositories.auth_repo import (
    id_exists,
    email_exists,
    phone_exists,
    insert_auth_code,
    get_valid_auth_code,
    mark_code_used,
    create_user,
    get_user_by_id,  # ✅ 로그인용
)
from helpers.sql_exec import get_connection  # 이미 프로젝트에 존재하는 헬퍼 가정

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^\d{9,15}$")  # 숫자만(하이픈 제거 후)
ID_RE    = re.compile(r"^[a-zA-Z0-9_\-\.]{4,32}$")

def _hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _clean_phone(p: str) -> str:
    return re.sub(r"[^0-9]", "", p or "")

# 1) 기본 유효성 + (선택) 중복체크
# 프런트 STEP1과 맞춤: us_id는 필수가 아님!
def verify_base_service(payload: dict):
    us_id    = (payload.get("us_id") or "").strip()          # 선택
    us_name  = (payload.get("us_name") or "").strip()        # 필수
    us_email = (payload.get("us_email") or "").strip().lower()  # 선택
    us_phone = _clean_phone(payload.get("us_phone"))         # 선택

    # 형식/필수
    if not us_name or len(us_name) < 2:
        return False, {"ok": False, "reason": "invalid_name"}
    if us_email and not EMAIL_RE.match(us_email):
        return False, {"ok": False, "reason": "invalid_email_format"}
    if us_phone and not PHONE_RE.match(us_phone):
        return False, {"ok": False, "reason": "invalid_phone_format"}
    if not (us_email or us_phone):
        return False, {"ok": False, "reason": "need_email_or_phone"}

    # us_id가 들어온 경우에만 중복/형식 확인
    if us_id:
        if not ID_RE.match(us_id):
            return False, {"ok": False, "reason": "invalid_id_format"}
        with get_connection() as conn:
            if id_exists(conn, us_id):
                return False, {"ok": False, "reason": "id_exists"}

    # (여기서는 이름+연락처 존재 여부를 실제 테이블에서 검증하려면
    #  repositories에 조회 함수를 추가해야 합니다. 현재 스키마 미정이라 통과 처리)
    return True, {"ok": True}

# 2) 인증 코드 전송 (Mock 전송, DB 저장)
def send_code_service(payload: dict):
    channel = (payload.get("channel") or "email").lower()  # email | sms
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

    code = f"{datetime.utcnow().microsecond % 1000000:06d}"  # 6자리
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    with get_connection() as conn:
        insert_auth_code(conn, channel, target, code, expires_at)

    # 개발 편의를 위해 code도 같이 반환(운영에서는 제거!)
    return True, {"ok": True, "dev_code": code, "expires_in_sec": 300}

# 3) 인증 코드 검증
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

# 4) 아이디 중복 체크
def check_id_service(payload: dict):
    us_id = (payload.get("us_id") or payload.get("id") or "").strip()
    if not ID_RE.match(us_id):
        return False, {"ok": False, "reason": "invalid_id_format"}
    with get_connection() as conn:
        exists = id_exists(conn, us_id)
    return True, {"ok": True, "exists": bool(exists)}

# 5) 회원 등록
def register_member_service(payload: dict):
    us_id    = (payload.get("us_id") or "").strip()
    us_pass  = (payload.get("us_pass") or "").strip()
    us_name  = (payload.get("us_name") or "").strip()
    us_email = (payload.get("us_email") or "").strip().lower()
    us_phone = _clean_phone(payload.get("us_phone"))
    us_role  = (payload.get("us_role") or "member").strip()

    # 필수/형식
    if not (us_id and us_pass and us_name):
        return False, {"ok": False, "reason": "missing_fields"}
    if not ID_RE.match(us_id):
        return False, {"ok": False, "reason": "invalid_id_format"}
    if us_email and not EMAIL_RE.match(us_email):
        return False, {"ok": False, "reason": "invalid_email_format"}
    if us_phone and not PHONE_RE.match(us_phone):
        return False, {"ok": False, "reason": "invalid_phone_format"}

    with get_connection() as conn:
        # 중복 확인
        if id_exists(conn, us_id):
            return False, {"ok": False, "reason": "id_exists"}
        if us_email and email_exists(conn, us_email):
            return False, {"ok": False, "reason": "email_exists"}
        if us_phone and phone_exists(conn, us_phone):
            return False, {"ok": False, "reason": "phone_exists"}

        hashed = _hash_sha256(us_pass)
        us_no = create_user(conn, us_id, hashed, us_name, us_email, us_phone, us_role)

    return True, {"ok": True, "us_no": us_no}

# 6) 로그인
def login_service(payload: dict):
    us_id   = (payload.get("id") or payload.get("us_id") or "").strip()
    us_pass = (payload.get("password") or payload.get("us_pass") or "").strip()
    if not us_id or not us_pass:
        return False, {"reason": "MISSING_CREDENTIALS"}

    with get_connection() as conn:
        user = get_user_by_id(conn, us_id)
        if not user:
            return False, {"reason": "INVALID_USER"}
        if user["us_pass"] != _hash_sha256(us_pass):
            return False, {"reason": "INVALID_PASSWORD"}

        public_user = {
            "id": user["us_id"],
            "name": user["us_name"],
            "roles": [user.get("us_role") or "member"],
        }
        return True, {"user": public_user}

# 7) 세션 사용자 검증
def get_session_user_service(sess_user):
    if not isinstance(sess_user, dict):
        return None
    if not all(k in sess_user for k in ("id", "name", "roles")):
        return None
    return sess_user
