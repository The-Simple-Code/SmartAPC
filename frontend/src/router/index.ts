// D:\SmartApc\frontend\src\router\index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 우선 alias 문제를 피하려면 아래 두 줄을 상대경로로 바꿔도 됩니다.
// import LoginView from '@/views/LoginView.vue'
// import HomeView from '@/views/HomeView.vue'

const routes = [
  { path: '/', redirect: '/login' }, // ✅ 첫 진입은 무조건 로그인으로
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') }, // 우선 상대경로로 안전하게
  { path: '/home', name: 'home', component: () => import('../views/HomeView.vue'), meta: { requiresAuth: true } },
  { path: '/signup', name: 'signup', component: () => import('../views/SignupView.vue') }, // ✅ 추가
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

let firstLoadChecked = false

router.beforeEach(async (to) => {
  const store = useUserStore()

  // 첫 로드 시 세션 체크 (실패해도 화면은 보여야 하므로 try/catch 없이 그대로)
  if (!firstLoadChecked) {
    firstLoadChecked = true
    try { await store.fetchMe() } catch (_) {}
  }

  // 보호 라우트는 로그인 필요
  if (to.meta.requiresAuth && !store.isAuthed) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // 로그인 페이지 접근 중 로그인 완료 상태면 홈으로
  if (to.name === 'login' && store.isAuthed) {
    return { name: 'home' }
  }

  // 그 외엔 통과
})

export default router
