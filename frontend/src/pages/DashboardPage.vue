<!-- D:\SmartApc\frontend\src\pages\DashboardPage.vue -->
<template>
  <!-- 배경 없음: App.vue의 회색 배경 상속 -->
  <div class="min-h-screen p-4 sm:p-6 text-slate-50">
    <div class="mx-auto max-w-7xl space-y-6">
      <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight whitespace-nowrap">대시보드</h1>
        <button class="w-full sm:w-auto px-4 py-2 rounded-xl bg-sky-600 text-white shadow hover:shadow-md transition whitespace-nowrap">새로고침</button>
      </header>

      <!-- 요약 카드 (밝은 카드 유지) -->
      <section class="grid gap-3 grid-cols-1 xs:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-2xl bg-white/85 backdrop-blur-md shadow-md p-4 sm:p-5 text-slate-900">
          <p class="text-xs sm:text-sm text-slate-600 whitespace-nowrap">오늘 입고</p>
          <p class="mt-1 sm:mt-2 text-2xl sm:text-3xl font-bold whitespace-nowrap">128</p>
          <p class="text-[11px] sm:text-xs text-slate-500 mt-1 whitespace-nowrap">+12 vs 어제</p>
        </div>
        <div class="rounded-2xl bg-white/85 backdrop-blur-md shadow-md p-4 sm:p-5 text-slate-900">
          <p class="text-xs sm:text-sm text-slate-600 whitespace-nowrap">실중량(kg)</p>
          <p class="mt-1 sm:mt-2 text-2xl sm:text-3xl font-bold whitespace-nowrap">4,920</p>
          <p class="text-[11px] sm:text-xs text-slate-500 mt-1 whitespace-nowrap">+3%</p>
        </div>
        <div class="rounded-2xl bg-white/85 backdrop-blur-md shadow-md p-4 sm:p-5 text-slate-900">
          <p class="text-xs sm:text-sm text-slate-600 whitespace-nowrap">파렛트 수</p>
          <p class="mt-1 sm:mt-2 text-2xl sm:text-3xl font-bold whitespace-nowrap">37</p>
          <p class="text-[11px] sm:text-xs text-slate-500 mt-1 whitespace-nowrap">-2</p>
        </div>
        <div class="rounded-2xl bg-white/85 backdrop-blur-md shadow-md p-4 sm:p-5 text-slate-900">
          <p class="text-xs sm:text-sm text-slate-600 whitespace-nowrap">알림</p>
          <p class="mt-1 sm:mt-2 text-2xl sm:text-3xl font-bold whitespace-nowrap">5</p>
          <p class="text-[11px] sm:text-xs text-slate-500 mt-1 whitespace-nowrap">처리 필요</p>
        </div>
      </section>

      <!-- 최근 입고 -->
      <section class="rounded-2xl bg-white/85 backdrop-blur-md shadow-md p-4 sm:p-6 text-slate-900">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <h2 class="text-lg font-semibold whitespace-nowrap">최근 입고</h2>
          <button class="text-sm text-sky-700 hover:underline whitespace-nowrap">전체 보기</button>
        </div>

        <!-- 모바일 카드 -->
        <div class="mt-4 sm:hidden space-y-3">
          <article v-for="n in 6" :key="n" class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <div class="flex items-center justify-between">
              <div class="font-semibold text-slate-900 whitespace-nowrap">S251031000{{ n }}</div>
              <span class="text-xs text-slate-500 whitespace-nowrap">2025-10-31</span>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-2 text-sm text-slate-600">
              <div class="whitespace-nowrap">농가: 한강농원</div>
              <div class="whitespace-nowrap">품종: 부사</div>
              <div class="col-span-2 whitespace-nowrap">중량: 78{{ n }} kg</div>
            </div>
          </article>
        </div>

        <!-- PC 테이블 -->
        <div class="mt-4 overflow-x-auto hidden sm:block">
          <table class="w-full text-sm text-slate-700">
            <thead class="text-slate-500 border-b border-slate-200 sticky top-0 bg-white/85 backdrop-blur">
              <tr class="text-left">
                <th class="py-2 pr-4 whitespace-nowrap">입고번호</th>
                <th class="py-2 pr-4 whitespace-nowrap">농가</th>
                <th class="py-2 pr-4 whitespace-nowrap">품종</th>
                <th class="py-2 pr-4 whitespace-nowrap">중량(kg)</th>
                <th class="py-2 whitespace-nowrap">일자</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 6" :key="n" class="border-b border-slate-100 hover:bg-slate-50/60">
                <td class="py-2 pr-4 whitespace-nowrap">S251031000{{ n }}</td>
                <td class="py-2 pr-4 whitespace-nowrap">한강농원</td>
                <td class="py-2 pr-4 whitespace-nowrap">부사</td>
                <td class="py-2 pr-4 whitespace-nowrap">{{ 780 + n }}</td>
                <td class="py-2 whitespace-nowrap">2025-10-31</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>
