<!-- D:\SmartApc\frontend\src\views\LoginView.vue -->
<template>
  <!-- 배경: 안전한 인라인 스타일(임의 속성 클래스 제거) -->
  <div class="min-h-svh relative overflow-hidden bg-gradient-to-br from-sky-50 via-white to-indigo-50">
    <div class="pointer-events-none absolute inset-0 opacity-60"
         style="background:
           radial-gradient(1200px 600px at -10% -10%, rgba(99,102,241,0.15), transparent),
           radial-gradient(800px 400px at 110% 110%, rgba(56,189,248,0.18), transparent);"></div>

    <!-- 중앙 컨테이너 -->
    <div class="relative z-10 flex min-h-svh items-center justify-center p-6">
      <div class="w-full max-w-md rounded-3xl border border-white/50 bg-white/70 backdrop-blur-md shadow-xl ring-1 ring-black/5">
        <!-- 헤더 -->
        <div class="px-8 pt-8 pb-4 text-center">
          <div
            class="mx-auto mb-4 flex h-12 w-12 select-none items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-md"
            aria-hidden="true" title="로그인">
            <!-- 🔒 자물쇠 아이콘 -->
            <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 11V8a5 5 0 0 0-10 0v3" />
              <rect x="5" y="11" width="14" height="9" rx="2" ry="2" />
              <path d="M12 15v2" />
            </svg>
          </div>
          <h1 class="text-xl font-semibold text-gray-900">SmartAPC</h1>
          <p class="mt-1 text-sm text-gray-500">계정으로 로그인해 주세요</p>
        </div>

        <!-- 폼 -->
        <form @submit.prevent="onSubmit" class="px-8 pb-6 space-y-4" aria-describedby="login-hint">
          <!-- 아이디 -->
          <div>
            <label for="login-id" class="mb-1 block text-sm font-medium text-gray-700">아이디</label>
            <div :class="['group relative flex items-center rounded-2xl ring-1 bg-white shadow-sm', error ? 'ring-2 ring-red-300' : 'ring-gray-200 focus-within:ring-2 focus-within:ring-indigo-500']">
              <span class="pl-3 text-gray-400" aria-hidden="true" title="사용자 아이디">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Z" />
                  <path d="M4 20a8 8 0 0 1 16 0" />
                </svg>
              </span>
              <input
                id="login-id"
                v-model.trim="id"
                placeholder="예: super 또는 user"
                class="peer w-full rounded-2xl bg-transparent px-3 py-3 text-gray-900 outline-none placeholder:text-gray-400"
                autocomplete="username" inputmode="text" required :aria-invalid="!!error" />
            </div>
          </div>

          <!-- 비밀번호 -->
          <div>
            <div class="mb-1 flex flex-wrap items-center justify-between gap-2">
              <RouterLink
                to="/signup"
                class="order-1 rounded-lg bg-indigo-50 px-3 py-1.5 text-xs font-medium text-indigo-700 hover:bg-indigo-100"
                title="회원등록">회원등록</RouterLink>

              <div class="order-2 ml-auto flex items-center gap-3">
                <label for="login-pw" class="block text-sm font-medium text-gray-700">비밀번호</label>
                <button type="button" class="text-xs text-gray-500 hover:text-gray-700"
                        @click="toggleShowPass" :aria-pressed="showPass"
                        :aria-label="showPass ? '비밀번호 숨기기' : '비밀번호 보기'"
                        :title="showPass ? '비밀번호 숨기기' : '비밀번호 보기'">
                  {{ showPass ? '숨기기' : '보기' }}
                </button>
              </div>
            </div>

            <div :class="['group relative flex items-center rounded-2xl ring-1 bg-white shadow-sm', error ? 'ring-2 ring-red-300' : 'ring-gray-200 focus-within:ring-2 focus-within:ring-indigo-500']">
              <span class="pl-3 text-gray-400" aria-hidden="true" title="비밀번호">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M7 14a5 5 0 1 1 4.9 4H11l-2 2H7l-1-1v-2l2-2" />
                  <circle cx="12" cy="9" r="1.5" />
                </svg>
              </span>
              <input
                id="login-pw"
                :type="showPass ? 'text' : 'password'"
                v-model="password"
                placeholder="데모 비밀번호: 1234"
                class="peer w-full rounded-2xl bg-transparent px-3 py-3 text-gray-900 outline-none placeholder:text-gray-400"
                autocomplete="current-password" required :aria-invalid="!!error"
                @keyup="onCaps($event)" @keydown="onCaps($event)" />
              <span class="pointer-events-none absolute right-3 inline-flex items-center text-gray-400" aria-hidden="true">
                <svg v-if="!showPass" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
                <svg v-else class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M3 3l18 18M10.6 10.6A3 3 0 0 0 12 15a3 3 0 0 0 3-3c0-.4-.1-.8-.2-1.1M9 5.5A10.4 10.4 0 0 1 12 5c6 0 10 7 10 7a18.4 18.4 0 0 1-3.2 3.9m-3 2A10.9 10.9 0 0 1 12 19c-6 0-10-7-10-7a19.6 19.6 0 0 1 3.6-4.3"/>
                </svg>
              </span>
            </div>
            <p v-show="caps" class="mt-1 text-xs text-amber-600">Caps Lock이 켜져 있습니다.</p>
          </div>

          <!-- 옵션 & 링크 -->
          <div class="flex items-center justify-between text-sm">
            <label class="inline-flex select-none items-center gap-2 text-gray-600">
              <input v-model="remember" type="checkbox" class="size-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
              <span>자동 로그인</span>
            </label>
            <a class="text-indigo-600 hover:text-indigo-700 hover:underline cursor-pointer">비밀번호 찾기</a>
          </div>

          <!-- 오류 -->
          <p v-if="error" class="rounded-xl bg-red-50 px-4 py-2 text-sm text-red-700 ring-1 ring-red-200" role="alert" aria-live="assertive" id="login-error">
            {{ error }}
          </p>

          <!-- 버튼 -->
          <button
            class="group relative inline-flex w-full items-center justify-center gap-2 rounded-2xl bg-indigo-600 px-4 py-3 font-medium text-white shadow-lg shadow-indigo-600/20 transition
                   hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:cursor-not-allowed disabled:bg-indigo-300"
            :disabled="loading || id.length===0 || password.length===0">
            <span v-if="!loading">로그인</span>
            <span v-else class="inline-flex items-center gap-2">
              <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 0 1 8-8v4a4 4 0 0 0-4 4H4z"/>
              </svg>
              로그인 중…
            </span>
          </button>

          <p id="login-hint" class="sr-only">아이디와 비밀번호를 입력한 뒤 로그인 버튼을 누르세요.</p>

          <!-- 푸터 -->
          <div class="pt-2 text-center text-xs text-gray-500">
            <span>© {{ year }} SmartAPC · 모두의 생산성을 위해</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// D:\SmartApc\frontend\src\views\LoginView.vue
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'   // ← 아래 2) stub 파일을 반드시 두면 안전합니다.

const router = useRouter()
const route = useRoute()
const store = useUserStore()

const id = ref(''); const password = ref('')
const showPass = ref(false)
const remember = ref(true)
const loading = ref(false)
const error = ref('')
const caps = ref(false)
const year = new Date().getFullYear()

onMounted(() => {
  queueMicrotask(() => {
    document.querySelector<HTMLInputElement>('input[autocomplete="username"]')?.focus()
  })
})

const toggleShowPass = () => { showPass.value = !showPass.value }
const onCaps = (e: KeyboardEvent) => {
  // @ts-ignore
  const state = e.getModifierState?.('CapsLock')
  if (typeof state === 'boolean') caps.value = state
}

const onSubmit = async () => {
  if (loading.value) return
  error.value = ''
  loading.value = true
  try {
    await store.login(id.value, password.value)
    // 'home' 라우트 없을 때 안전하게 루트로 보냄
    const redirect = (route.query.redirect as string) || '/'
    router.replace(redirect)
  } catch {
    error.value = '아이디 또는 비밀번호를 확인하세요.'
  } finally {
    loading.value = false
  }
}
</script>
