<!-- D:\SmartApc\frontend\src\pages\FormPage.vue -->
<template>
  <div class="min-h-screen p-4 sm:p-6 text-slate-50">
    <div class="mx-auto max-w-3xl">
      <section class="rounded-2xl bg-white/90 backdrop-blur-md shadow-md p-5 sm:p-6 text-slate-900">
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight whitespace-nowrap">입고 등록</h1>

        <form class="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-slate-600 mb-1 whitespace-nowrap">농가</label>
            <input class="w-full px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-200 bg-white" placeholder="농가명" />
          </div>
          <div>
            <label class="block text-sm text-slate-600 mb-1 whitespace-nowrap">품종</label>
            <input class="w-full px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-200 bg-white" placeholder="품종명" />
          </div>
          <div>
            <label class="block text-sm text-slate-600 mb-1 whitespace-nowrap">입고일자</label>
            <input type="date" class="w-full px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-200 bg-white" />
          </div>
          <div>
            <label class="block text-sm text-slate-600 mb-1 whitespace-nowrap">중량(kg)</label>
            <input type="number" class="w-full px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-200 bg-white" />
          </div>

          <div class="sm:col-span-2">
            <label class="block text-sm text-slate-600 mb-1 whitespace-nowrap">비고</label>
            <textarea rows="4" class="w-full px-3 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-200 bg-white" placeholder="메모"></textarea>
          </div>

          <div class="sm:col-span-2 flex flex-col sm:flex-row justify-end gap-2">
            <button type="button" class="px-4 py-2 rounded-xl bg-white border border-slate-200 shadow hover:shadow-md whitespace-nowrap">취소</button>
            <button type="submit" class="px-4 py-2 rounded-xl bg-sky-600 text-white shadow hover:shadow-md whitespace-nowrap">저장</button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

