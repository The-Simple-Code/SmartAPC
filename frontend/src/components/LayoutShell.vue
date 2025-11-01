<!-- D:\SmartAPC\frontend\src\components\LayoutShell.vue -->
<template>
  <div class="min-h-screen grid md:grid-cols-[260px_1fr]">
    <!-- 사이드 내비 -->
    <aside class="hidden md:flex md:flex-col p-4 gap-3 bg-white/80 border-r border-slate-200">
      <div class="text-xl font-bold tracking-tight">🍍 SmartAPC</div>
      <nav class="flex-1 flex flex-col gap-1 mt-2 text-sm">
        <RouterLink to="/" class="nav-btn" :class="{ active: $route.name==='dashboard' }">대시보드</RouterLink>
        <RouterLink to="/table" class="nav-btn" :class="{ active: $route.name==='table' }">테이블</RouterLink>
        <RouterLink to="/form" class="nav-btn" :class="{ active: $route.name==='form' }">폼</RouterLink>
        <RouterLink to="/empty" class="nav-btn" :class="{ active: $route.name==='empty' }">빈 상태</RouterLink>
      </nav>
      <div class="text-xs text-slate-500">v0.1 · bright theme</div>
    </aside>

    <!-- 콘텐츠 영역 -->
    <main class="p-3 md:p-6">
      <!-- 상단 바 (모바일 포함) -->
      <header class="md:hidden mb-4">
        <div class="glass rounded-xl p-3 flex items-center justify-between">
          <div class="font-semibold">🍍 SmartAPC</div>
          <button class="px-3 py-1 rounded-lg bg-slate-900 text-white">메뉴</button>
        </div>
      </header>

      <div class="max-w-7xl mx-auto">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.nav-btn { @apply px-3 py-2 rounded-xl hover:bg-slate-100 transition; }
.nav-btn.active { @apply bg-slate-900 text-white; }
</style>
