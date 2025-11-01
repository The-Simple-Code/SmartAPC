# D:\SmartAPC\backend\migrations\env.py
from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ─────────────────────────────────────────────────────────────
# 1) 로깅 설정
# ─────────────────────────────────────────────────────────────
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ─────────────────────────────────────────────────────────────
# 2) .env 로드 및 SQLAlchemy URL 주입
# ─────────────────────────────────────────────────────────────
# .env: D:\SmartAPC\backend\.env
from dotenv import load_dotenv

# backend/.env 로드
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

db_url = os.getenv("DATABASE_URL", "").strip()
if not db_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Please create D:\\SmartAPC\\backend\\.env and set DATABASE_URL"
    )
# alembic.ini 의 sqlalchemy.url 대신 .env 값을 주입
config.set_main_option("sqlalchemy.url", db_url)

# ─────────────────────────────────────────────────────────────
# 3) Flask 앱/DB 메타데이터 연결
# ─────────────────────────────────────────────────────────────
# 앱 팩토리/DB 인스턴스를 통해 메타데이터를 사용
from app import create_app
from app.extensions.db import db

# 모델을 반드시 import 해서 메타데이터에 등록 (자동생성용)
# 필요한 모델들을 import 하세요. (여기서는 DeviceSetting 예시)
from app.models import device_setting  # noqa: F401

# Alembic이 참조할 메타데이터
target_metadata = db.metadata

# ─────────────────────────────────────────────────────────────
# 4) Offline / Online 런 모드
# ─────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,      # 타입 변경 감지
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # config.get_section은 sqlalchemy.* 옵션을 dict로 반환
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Flask 앱 컨텍스트 안에서 메타데이터 인식
    app = create_app()
    with app.app_context():
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,           # 타입 변경 감지
                compare_server_default=True, # 서버 기본값 변경 감지
            )
            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
