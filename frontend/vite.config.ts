// D:\SmartApc\frontend\vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import tailwindcss from '@tailwindcss/vite' // Tailwind v4용 플러그인

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: {
    host: true,                 // 동일 네트워크/공인 IP 접근 허용
    strictPort: true,           // 포트 충돌 시 자동 변경 방지(예측 가능)
    port: 5173,
    proxy: {
      // 프론트에서는 '/api'로만 호출 → Vite가 백엔드(5000)로 프록시
      '/api': { target: 'http://127.0.0.1:5000', changeOrigin: true },
    },
    // 🔧 외부 IP(예: 211.42.144.32, 192.168.x.x)로 접속할 때 HMR 끊김 방지
    hmr: {
      host: 'localhost',        // 개발PC에서 구동 → 클라이언트가 WS 연결할 호스트
      clientPort: 5173,         // 방화벽/프록시로 포트 변경 시 맞춰 조정
    },
  },
  // 디버깅 편의(빌드 시 소스맵 생성) — 필요 없으면 지워도 됨
  build: {
    sourcemap: true,
  },
})
