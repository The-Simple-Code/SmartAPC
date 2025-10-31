# SmartAPC 폴더/기본 파일 생성 스크립트 (Windows PowerShell)
# 실행: PowerShell에서 아래 중 하나로 실행
#   1) 현재 세션만 허용:  powershell -ExecutionPolicy Bypass -File "D:\SmartAPC\scripts\init-folders.ps1"
#   2) 프로세스 범위 허용:  Set-ExecutionPolicy -Scope Process Bypass; . "D:\SmartAPC\scripts\init-folders.ps1"

$ErrorActionPreference = "Stop"

function New-Dir($path) {
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "DIR  + $path"
    } else {
        Write-Host "DIR  = $path (exists)"
    }
}

function New-File($path, $content = "") {
    $parent = Split-Path -Parent $path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
    if (-not (Test-Path -LiteralPath $path)) {
        $content | Out-File -FilePath $path -Encoding UTF8 -Force
        Write-Host "FILE + $path"
    } else {
        Write-Host "FILE = $path (exists)"
    }
}

$Root = "D:\SmartAPC"

# ─────────────────────────────────────────────────────────────
# 디렉터리 생성
# ─────────────────────────────────────────────────────────────
$dirs = @(
    "$Root\backend\app\extensions",
    "$Root\backend\app\models",
    "$Root\backend\app\repositories",
    "$Root\backend\app\services",
    "$Root\backend\app\routes",
    "$Root\backend\app\schemas",
    "$Root\backend\app\utils",
    "$Root\backend\migrations",

    "$Root\frontend\src\assets",
    "$Root\frontend\src\components",
    "$Root\frontend\src\pages",
    "$Root\frontend\src\layouts",
    "$Root\frontend\src\stores",
    "$Root\frontend\src\services",

    "$Root\docs",
    "$Root\scripts"
)

foreach ($d in $dirs) { New-Dir $d }

# ─────────────────────────────────────────────────────────────
# backend 기본 파일 (__init__.py 포함)
# ─────────────────────────────────────────────────────────────
New-File "$Root\backend\app\__init__.py" @'
"""
SmartAPC Flask App Factory (stub)
"""
from flask import Flask

def create_app(config_name: str = "development"):
    app = Flask(__name__)
    # NOTE: 실제 설정/확장/블루프린트 등록은 이후 단계에서 추가
    return app
'@

New-File "$Root\backend\app\config.py" @'
import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

def get_config(name: str):
    return DevelopmentConfig if name == "development" else ProductionConfig
'@

# __init__.py (패키지 인식용) - 얇게 생성
$initTargets = @(
    "$Root\backend\app\extensions\__init__.py",
    "$Root\backend\app\models\__init__.py",
    "$Root\backend\app\repositories\__init__.py",
    "$Root\backend\app\services\__init__.py",
    "$Root\backend\app\routes\__init__.py",
    "$Root\backend\app\schemas\__init__.py",
    "$Root\backend\app\utils\__init__.py"
)
foreach ($p in $initTargets) { New-File $p "# package stub`n" }

# extensions stubs
New-File "$Root\backend\app\extensions\db.py" @'
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
'@
New-File "$Root\backend\app\extensions\mail.py" @'
from flask_mail import Mail
mail = Mail()
'@
New-File "$Root\backend\app\extensions\sms.py" @'
class SMSClient:
    def __init__(self):
        self.provider = None
        self.api_key = None
        self.api_secret = None
    def init_app(self, app):
        self.provider = app.config.get("SMS_PROVIDER", "mock")
        self.api_key = app.config.get("SMS_API_KEY", "")
        self.api_secret = app.config.get("SMS_API_SECRET", "")
    def send(self, to: str, text: str) -> bool:
        print(f"[SMS:{self.provider}] -> {to}: {text}")
        return True

sms_client = SMSClient()
'@

# wsgi stub
New-File "$Root\backend\app\wsgi.py" @'
from . import create_app
app = create_app()
'@

# requirements & env example
New-File "$Root\backend\requirements.txt" @'
flask
flask-sqlalchemy
flask-mail
pyodbc
sqlalchemy
'@

New-File "$Root\backend\.env.example" @'
SECRET_KEY=change-me
DATABASE_URL=mssql+pyodbc://user:pass@HOST/DBNAME?driver=ODBC+Driver+17+for+SQL+Server
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your@email
MAIL_PASSWORD=your-password
SMS_PROVIDER=mock
SMS_API_KEY=
SMS_API_SECRET=
'@

# ─────────────────────────────────────────────────────────────
# frontend 최소 파일
# ─────────────────────────────────────────────────────────────
New-File "$Root\frontend\index.html" @'
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SmartAPC</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
'@

New-File "$Root\frontend\src\main.ts" @'
console.log("SmartAPC frontend bootstrap (stub)");
'@

New-File "$Root\frontend\src\App.vue" @'
<template>
  <main class="p-4">SmartAPC App (stub)</main>
</template>
'@

New-File "$Root\frontend\tailwind.config.js" "// tailwind config (to be filled)\n"
New-File "$Root\frontend\postcss.config.js" "// postcss config (to be filled)\n"
New-File "$Root\frontend\vite.config.ts" "// vite config (to be filled)\n"
New-File "$Root\frontend\.env.example" "VITE_API_BASE=http://127.0.0.1:5000\n"

# ─────────────────────────────────────────────────────────────
# docs
# ─────────────────────────────────────────────────────────────
New-File "$Root\docs\template.md" @'
# ?? SmartAPC 개발 문서
- 작성일: YYYY-MM-DD
- 작성자: rock_crasher
- 프로젝트 경로: D:\SmartAPC
- 구성요소: Flask + Tailwind + MS SQL Server
- 목적: <이 문서의 목적 요약>

## ?? 주요 변경 요약 (Summary)
| 구분 | 설명 |
|------|------|
| 작업 유형 |  |
| 변경 위치 |  |
| 관련 기능 |  |
| 주요 의도 |  |
| 결과 |  |

## ?? 상세 설명 (Details)
(상세 내용 기입)
'@

New-File "$Root\docs\decisions.md" "# Architecture Decisions (ADRs)\n"

Write-Host "`n완료: SmartAPC 기본 폴더와 스텁 파일이 준비되었습니다." -ForegroundColor Green
