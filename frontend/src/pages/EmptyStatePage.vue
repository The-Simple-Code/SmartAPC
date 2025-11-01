<!-- D:\SmartApc\frontend\src\pages\EmptyStatePage.vue -->
<template>
  <div class="min-h-screen p-4 sm:p-6 text-slate-50">
    <div class="mx-auto max-w-3xl">
      <section class="rounded-2xl bg-white/90 backdrop-blur-md shadow-md p-8 sm:p-10 text-center text-slate-900">
        <div class="mx-auto mb-4 flex h-16 w-16 sm:h-20 sm:w-20 items-center justify-center rounded-2xl bg-slate-100 shadow">
          <span class="text-3xl sm:text-4xl">✨</span>
        </div>

        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight whitespace-nowrap">아직 데이터가 없어요</h1>
        <p class="mt-2 text-slate-600 text-sm sm:text-base">
          첫 항목을 추가하면 여기에서 진행 현황과 통계를 한눈에 볼 수 있어요.
        </p>

        <div class="mt-6 flex flex-col sm:flex-row gap-2 justify-center">
          <RouterLink to="/form"  class="px-5 py-3 rounded-xl bg-sky-600 text-white shadow hover:shadow-lg transition whitespace-nowrap">새로 등록하기</RouterLink>
          <RouterLink to="/table" class="px-5 py-3 rounded-xl bg-white border border-slate-200 shadow hover:shadow-md transition whitespace-nowrap">목록으로 이동</RouterLink>
        </div>
      </section>
    </div>
  </div>
</template>
