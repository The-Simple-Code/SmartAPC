// D:\SmartApc\frontend\src\stores\user.ts
import { defineStore } from 'pinia'

const API = import.meta.env.VITE_API_BASE ?? '/api'   // ← 기본값을 '/api'로 (Vite 프록시 사용)
type User = { id: string; name: string; roles: string[] } | null

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User,
    loading: false,
  }),
  getters: {
    isAuthed: (s) => !!s.user,
  },
  actions: {
    async fetchMe() {
      this.loading = true
      try {
        const res = await fetch(`${API}/api/auth/me`, {
          method: 'GET',
          credentials: 'include',
        })
        const data = await res.json().catch(() => ({}))
        this.user = data?.ok ? (data.user as User) : null
      } finally {
        this.loading = false
      }
    },
    async login(id: string, password: string) {
      const res = await fetch(`${API}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ id, password }),
      })
      const data = await res.json().catch(() => ({}))
      if (!res.ok || !data.ok) throw new Error(data.error || 'LOGIN_FAILED')
      this.user = data.user as User
    },
    async logout() {
      await fetch(`${API}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      })
      this.user = null
    },
  },
})
