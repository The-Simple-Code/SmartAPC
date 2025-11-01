# D:\SmartApc\backend\app\repositories\auth_repo.py
from sqlalchemy import text

def id_exists(conn, us_id: str):
    row = conn.execute(text("SELECT 1 FROM dbo.tbl_users WHERE us_id=:us_id"), {"us_id": us_id}).fetchone()
    return bool(row)

def email_exists(conn, email: str):
    row = conn.execute(text("SELECT 1 FROM dbo.tbl_users WHERE us_email=:email"), {"email": email}).fetchone()
    return bool(row)

def phone_exists(conn, phone: str):
    row = conn.execute(text("SELECT 1 FROM dbo.tbl_users WHERE us_phone=:phone"), {"phone": phone}).fetchone()
    return bool(row)

def insert_auth_code(conn, channel: str, target: str, code: str, expires_at):
    conn.execute(
        text("""INSERT INTO dbo.AuthCode(channel,target,code,expires_at,used) 
                VALUES(:c,:t,:code,:exp,0)"""),
        {"c": channel, "t": target, "code": code, "exp": expires_at},
    )
    conn.commit()

def get_valid_auth_code(conn, channel: str, target: str, code: str):
    return conn.execute(
        text("""SELECT TOP 1 ac_id, channel, target, code, expires_at, used
                FROM dbo.AuthCode
                WHERE channel=:c AND target=:t AND code=:code AND used=0 AND expires_at>GETUTCDATE()
                ORDER BY ac_id DESC"""),
        {"c": channel, "t": target, "code": code},
    ).mappings().fetchone()

def mark_code_used(conn, ac_id: int):
    conn.execute(text("UPDATE dbo.AuthCode SET used=1 WHERE ac_id=:id"), {"id": ac_id})
    conn.commit()

def create_user(conn, us_id, us_pass, us_name, us_email, us_phone, us_role):
    row = conn.execute(
        text("""INSERT INTO dbo.tbl_users(us_id,us_pass,us_name,us_email,us_phone,us_role) 
                OUTPUT INSERTED.us_no
                VALUES(:id,:pw,:nm,:em,:ph,:rl)"""),
        {"id": us_id, "pw": us_pass, "nm": us_name, "em": us_email, "ph": us_phone, "rl": us_role},
    ).fetchone()
    conn.commit()
    return row[0]

def get_user_by_id(conn, us_id: str):
    row = conn.execute(
        text("""SELECT TOP 1 us_no, us_id, us_pass, us_name, us_email, us_phone, us_role, us_created
                FROM dbo.tbl_users
                WHERE us_id=:id"""),
        {"id": us_id},
    ).mappings().fetchone()
    return dict(row) if row else None
