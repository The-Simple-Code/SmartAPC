<!-- D:\SmartApc\README.md -->

<p align="center">
  <img src="https://raw.githubusercontent.com/The-Simple-Code/SmartAPC/main/frontend/src/assets/logo-smartapc.png" alt="SmartAPC Logo" width="220" />
</p>

<h1 align="center">🍍 SmartAPC</h1>

<p align="center">
  <em>스마트 농산물 선별·입출고 관리 시스템</em><br>
  <strong>Flask + Vue 3 + Tailwind v4 기반의 차세대 WebAdmin 프로젝트</strong>
</p>

<p align="center">
  <a href="https://github.com/The-Simple-Code/SmartAPC/actions">
    <img src="https://github.com/The-Simple-Code/SmartAPC/actions/workflows/backend.yml/badge.svg" alt="Backend Build Status">
  </a>
  <a href="https://github.com/The-Simple-Code/SmartAPC/actions">
    <img src="https://github.com/The-Simple-Code/SmartAPC/actions/workflows/frontend.yml/badge.svg" alt="Frontend Build Status">
  </a>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Node.js-18%2B-339933?logo=node.js&logoColor=white" alt="Node.js 18+">
  <img src="https://img.shields.io/badge/Vue-3.5-42b883?logo=vue.js&logoColor=white" alt="Vue 3.5">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

---

## 📂 Project Structure
D:\SmartApc
│
├── backend/ # Flask REST API backend
│ ├── app/
│ │ ├── init.py # Flask 앱 팩토리
│ │ ├── wsgi.py # Waitress 실행 진입점
│ │ ├── routes/ # Blueprint 라우트 폴더
│ │ │ ├── auth_routes.py # 회원등록/로그인 API
│ │ │ └── health.py # 헬스체크 API
│ │ ├── services/ # 비즈니스 로직 계층
│ │ │ └── auth_service.py # 인증 서비스 로직
│ │ ├── repositories/ # DB 접근 계층
│ │ │ └── auth_repo.py # 사용자/코드 관련 쿼리
│ │ └── helpers/ # 공통 유틸리티
│ │ └── sql_exec.py # pyodbc 연결 헬퍼
│ ├── database/ddl/ # SQL 테이블 DDL
│ ├── requirements.txt # 필수 패키지 목록
│ ├── requirements_full_backup.txt
│ └── .vscode/ # 디버깅 설정
│
├── frontend/ # Vue 3 + Vite Frontend
│ ├── src/
│ │ ├── views/
│ │ │ ├── LoginView.vue # 로그인 화면
│ │ │ └── SignupView.vue # 회원등록(3단계)
│ │ ├── stores/user.ts # Pinia 사용자 상태관리
│ │ ├── router/index.ts # Vue Router
│ │ └── assets/, components/
│ ├── package.json # 프론트엔드 패키지 목록
│ ├── vite.config.ts # 프록시 포함 Vite 설정
│ ├── .env.development.local # VITE_API_BASE=/api
│ └── tsconfig.json
│
├── SmartApc.code-workspace # VSCode 워크스페이스
└── README.md # 본 문서

yaml
코드 복사

---

## 🧰 Tech Stack

### 🖥️ Frontend
- Vue 3.5 (Composition API / `<script setup>`)
- Vite 7
- Tailwind CSS v4
- Pinia 3
- Vue Router 4
- TypeScript

### ⚙️ Backend
- Flask 3.0
- Flask-CORS
- SQLAlchemy 2.0
- pyodbc (MS SQL Server)
- Waitress (Windows 배포용)
- python-dotenv (.env 설정)

---

## 🧩 Features

### ✅ 회원등록 (Signup)
3단계 시뮬레이션 기반 인증 흐름  
1. **DB 인증 (Step 1)** – 이름/이메일/전화번호 검증  
2. **본인 인증 (Step 2)** – 인증번호 전송(시뮬레이션) → 코드 입력 시 자동 3단계 전환  
3. **회원등록 (Step 3)** – 아이디 중복확인 + 비밀번호 설정 → 등록 완료  

### 🔐 로그인 (Login)
- 아이디/비밀번호 입력
- Caps Lock 감지
- 비밀번호 보기 토글
- 회원등록 페이지 링크 포함

---

## ⚙️ Installation Guide

### Backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

# 실행
$env:FLASK_APP="app.wsgi"
$env:FLASK_ENV="development"
python -m flask run --host=127.0.0.1 --port=5000
Frontend
bash
코드 복사
cd frontend
npm install
npm run dev
👉 접속: http://localhost:5173

🌍 Environment
frontend/.env.development.local

ini
코드 복사
VITE_API_BASE=/api
backend/.env

ini
코드 복사
SECRET_KEY=dev-secret-key
DATABASE_URL=mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+18+for+SQL+Server
🧾 Requirements Summary
Frontend (package.json)
Vue 3.5 / Vite 7 / Tailwind 4 / Pinia 3 / Vue Router 4

Backend (requirements.txt)
ini
코드 복사
Flask==3.0.3
Flask-Cors==4.0.1
python-dotenv==1.0.1
SQLAlchemy==2.0.35
greenlet==3.1.1
pyodbc==5.1.0
waitress==3.0.0
🔀 Git Workflow
bash
코드 복사
git checkout -b feature/signup-outline
git add .
git commit -m "Add signup 3-step simulation flow"
git remote add origin https://github.com/The-Simple-Code/SmartAPC.git
git push -u origin feature/signup-outline
🧭 Next Steps
✅ 회원등록 Step 3 → 실제 DB 저장 연동 (register_member_service)

✅ 로그인 API 연동 (/api/auth/login)

🧱 메인 대시보드 (HomeView) 구현

⚙️ Device 설정 관리 기능 통합

<p align="center"> <strong>© 2025 SmartAPC – Productivity for Smart Agriculture 🌾</strong><br> <a href="https://github.com/The-Simple-Code/SmartAPC">github.com/The-Simple-Code/SmartAPC</a> </p> ```