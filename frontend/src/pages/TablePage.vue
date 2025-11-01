<!-- D:\SmartApc\frontend\src\pages\TablePage.vue -->
<template>
  <div class="min-h-screen p-4 sm:p-6 text-slate-50">
    <div class="mx-auto max-w-7xl">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight whitespace-nowrap">입고 내역</h1>
        <div class="flex flex-col xs:flex-row gap-2 w-full xs:w-auto overflow-x-auto">
          <input
            placeholder="검색..."
            class="w-full xs:w-56 px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-200 bg-white/90 text-slate-900"
          />
          <div class="flex gap-2">
            <button class="flex-1 xs:flex-none px-4 py-2 rounded-xl bg-white border border-slate-200 shadow hover:shadow-md whitespace-nowrap text-slate-900">엑셀</button>
            <button class="flex-1 xs:flex-none px-4 py-2 rounded-xl bg-sky-600 text-white shadow hover:shadow-md whitespace-nowrap">신규</button>
          </div>
        </div>
      </div>

      <!-- 모바일 카드 -->
      <div class="mt-4 space-y-3 sm:hidden">
        <article v-for="n in 12" :key="n" class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm text-slate-800">
          <div class="flex items-center justify-between">
            <div class="font-semibold whitespace-nowrap">S251031000{{ n }}</div>
            <span class="text-xs text-slate-500 whitespace-nowrap">A-01</span>
          </div>
          <div class="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-sm text-slate-600">
            <div class="whitespace-nowrap">농가: 한강농원</div>
            <div class="whitespace-nowrap">품종: 후지</div>
            <div class="whitespace-nowrap">중량: {{ 700 + n }} kg</div>
            <div class="whitespace-nowrap">파렛트: {{ Math.ceil(n/5) }}</div>
          </div>
          <div class="mt-3 flex gap-2">
            <button class="px-3 py-1.5 rounded-lg bg-white border border-slate-200 shadow hover:shadow-sm whitespace-nowrap">수정</button>
            <button class="px-3 py-1.5 rounded-lg bg-rose-600 text-white shadow hover:shadow-sm whitespace-nowrap">삭제</button>
          </div>
        </article>
      </div>

      <!-- PC 테이블 -->
      <div class="mt-4 rounded-2xl bg-white/90 backdrop-blur-md shadow-md overflow-hidden hidden sm:block text-slate-900">
        <div class="overflow-auto max-h/[70vh]">
          <table class="w-full text-sm">
            <thead class="sticky top-0 bg-white/90 backdrop-blur border-b border-slate-200">
              <tr class="text-left text-slate-500">
                <th class="px-3 py-2 whitespace-nowrap">입고번호</th>
                <th class="px-3 py-2 whitespace-nowrap">농가</th>
                <th class="px-3 py-2 whitespace-nowrap">품종</th>
                <th class="px-3 py-2 whitespace-nowrap">중량(kg)</th>
                <th class="px-3 py-2 whitespace-nowrap">파렛트</th>
                <th class="px-3 py-2 whitespace-nowrap">저장위치</th>
                <th class="px-3 py-2 whitespace-nowrap">액션</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 30" :key="n" class="border-b border-slate-100 hover:bg-slate-50/60">
                <td class="px-3 py-2 whitespace-nowrap">S251031000{{ n }}</td>
                <td class="px-3 py-2 whitespace-nowrap">한강농원</td>
                <td class="px-3 py-2 whitespace-nowrap">후지</td>
                <td class="px-3 py-2 whitespace-nowrap">{{ 700 + n }}</td>
                <td class="px-3 py-2 whitespace-nowrap">{{ Math.ceil(n/5) }}</td>
                <td class="px-3 py-2 whitespace-nowrap">A-01</td>
                <td class="px-3 py-2 whitespace-nowrap">
                  <div class="flex gap-2">
                    <button class="px-2 py-1 rounded-lg bg-white border border-slate-200 shadow hover:shadow-sm whitespace-nowrap">수정</button>
                    <button class="px-2 py-1 rounded-lg bg-rose-600 text-white shadow hover:shadow-sm whitespace-nowrap">삭제</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


