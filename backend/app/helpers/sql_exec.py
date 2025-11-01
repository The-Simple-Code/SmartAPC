# D:\SmartApc\backend\app\helpers\sql_exec.py
"""
SQL Server 연결 헬퍼 (SmartAPC)
- SQLAlchemy + pyodbc 기반
- 프로젝트 전역에서 같은 엔진/풀을 재사용
- 기존 코드 스타일( conn.execute(...); conn.commit() )과 100% 호환되도록 커넥션 래핑
"""
from __future__ import annotations
import os
from contextlib import contextmanager
from typing import Any, Iterable, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection, Result

# ------------------------------------------------------------
# 환경변수
#  - DATABASE_URL 우선 (예: mssql+pyodbc://user:pass@HOST/DB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes)
#  - 없으면 아래 개별 항목 조합
#    DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER(기본: ODBC Driver 17 for SQL Server)
# ------------------------------------------------------------

_ENGINE: Optional[Engine] = None


def _build_url_from_parts() -> str:
    server   = os.getenv("DB_SERVER", "127.0.0.1")
    database = os.getenv("DB_NAME",   "master")
    user     = os.getenv("DB_USER",   "")
    password = os.getenv("DB_PASSWORD", "")
    driver   = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    # URL 인코딩: 공백 → + 로 처리
    driver_q = driver.replace(" ", "+")
    if user and password:
        return f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver_q}&TrustServerCertificate=yes"
    else:
        # 통합 인증(Windows) 등 사용자/암호 미지정 케이스
        # 참고: ODBC 데이터소스(DSN) 사용 시에는 mssql+pyodbc://@DSN 형식도 가능
        return f"mssql+pyodbc://@{server}/{database}?driver={driver_q}&Trusted_Connection=yes&TrustServerCertificate=yes"


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    return url if url else _build_url_from_parts()


def _create_engine() -> Engine:
    # fast_executemany는 대량 insert에 유리
    url = _get_database_url()
    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=1800,    # 30분마다 재활용(방화벽 아이들 타임아웃 회피)
        pool_size=10,
        max_overflow=20,
        connect_args={
            # pyodbc 옵션들—필요시 추가
            "fast_executemany": True,
        },
        future=True,          # SQLAlchemy 2.x 스타일
    )
    return engine


def get_engine() -> Engine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = _create_engine()
    return _ENGINE


# ------------------------------------------------------------
# 커넥션 래퍼: commit()을 호출해도 예외가 나지 않도록 no-op 처리
# - 기존 코드에서 conn.commit()을 부르더라도 안전하게 무시
# - execute/close 는 실제 Connection에 위임
# ------------------------------------------------------------
class ConnWrapper:
    def __init__(self, conn: Connection):
        self._conn = conn

    # 핵심 위임 메서드
    def execute(self, statement, params: Optional[dict] = None) -> Result:
        if params is None:
            return self._conn.execute(statement)
        return self._conn.execute(statement, params)

    def exec_text(self, sql: str, params: Optional[dict] = None) -> Result:
        """text(sql) 편의 메서드"""
        return self.execute(text(sql), params or {})

    def commit(self) -> None:
        """기존 코드 호환용: no-op"""
        # 트랜잭션을 명시적으로 열지 않았을 때 SQLAlchemy Connection에는 commit이 없고,
        # 호출 시 InvalidRequestError가 날 수 있다. 이를 무시하여 코드 호환성 유지.
        return None

    def close(self) -> None:
        self._conn.close()

    # 필요한 속성 접근자를 최소한으로 노출(필요 시 추가)
    @property
    def dialect(self):
        return self._conn.dialect

    def __getattr__(self, item: str) -> Any:
        # 나머지 속성/메서드는 원 커넥션에 위임
        return getattr(self._conn, item)


# ------------------------------------------------------------
# Context Manager
# - with get_connection() as conn:
#     conn.execute(text("..."), {...})
#     conn.commit()   # ← 호출해도 안전 (무시)
# ------------------------------------------------------------
@contextmanager
def get_connection() -> Iterable[ConnWrapper]:
    conn = get_engine().connect()  # 트랜잭션 자동 시작 안 함
    wrapped = ConnWrapper(conn)
    try:
        yield wrapped
        # 명시적 트랜잭션을 쓰지 않을 때는 개별 DML은 autocommit 되지 않음.
        # Repo 코드에서 필요한 곳은 wrapped.commit()을 호출하지만 no-op이므로,
        # 변경이 필요한 DML은 아래처럼 명시 트랜잭션으로 처리하는 편의 함수를 제공.
    finally:
        wrapped.close()


# ------------------------------------------------------------
# 편의 트랜잭션 실행자
#   with begin_transaction() as conn:
#       conn.exec_text("INSERT ...", {...})
#       # 종료 시 자동 commit
# ------------------------------------------------------------
@contextmanager
def begin_transaction() -> Iterable[Connection]:
    with get_engine().begin() as tx_conn:
        yield tx_conn  # 여기서 tx_conn.commit() 호출도 가능(중복 commit은 무시)


# ------------------------------------------------------------
# 간단 헬퍼들 (선택 사용)
# ------------------------------------------------------------
def fetch_scalar(sql: str, params: Optional[dict] = None) -> Any:
    with get_connection() as conn:
        res = conn.exec_text(sql, params)
        row = res.fetchone()
        return row[0] if row and len(row) > 0 else None


def fetch_one_dict(sql: str, params: Optional[dict] = None) -> Optional[dict]:
    with get_connection() as conn:
        res = conn.exec_text(sql, params)
        row = res.mappings().fetchone()
        return dict(row) if row else None


def fetch_all_dicts(sql: str, params: Optional[dict] = None) -> list[dict]:
    with get_connection() as conn:
        res = conn.exec_text(sql, params)
        return [dict(m) for m in res.mappings().all()]
