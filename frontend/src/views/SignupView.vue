<!-- D:\SmartApc\frontend\src\views\SignupView.vue -->
<template>
  <!-- 배경: 로그인과 톤 맞춘 은은한 그라디언트 + 패턴 -->
  <div class="min-h-svh relative overflow-hidden bg-gradient-to-br from-sky-50 via-white to-indigo-50">
    <div class="pointer-events-none absolute inset-0 [background:radial-gradient(1200px_600px_at_-10%_-10%,theme(colors.indigo.100/.5),transparent),radial-gradient(800px_400px_at_110%_110%,theme(colors.sky.100/.6),transparent)]"></div>

    <!-- 카드 컨테이너 -->
    <div class="relative z-10 flex min-h-svh items-center justify-center p-6">
      <div class="relative w-full max-w-md rounded-3xl border border-white/50 bg-white/70 backdrop-blur-md shadow-xl ring-1 ring-black/5">
        <RouterLink
          to="/login"
          class="absolute left-4 bottom-4 text-sm text-indigo-700 hover:text-indigo-900 hover:underline"
        >로그인으로 이동</RouterLink>

        <!-- 헤더 -->
        <div class="px-8 pt-8 pb-4 flex items-center gap-3">
          <div class="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-indigo-600 text-white text-xl">🔑</div>
          <div>
            <h1 class="text-2xl font-bold text-slate-800">회원등록 (3단계)</h1>
            <p class="text-sm text-slate-500">시뮬레이션 본인 인증 · 직원/공선회 대상</p>
          </div>
        </div>

        <!-- 스텝 표시줄 -->
        <div class="px-8 pb-2 select-none">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div :class="circleClass(1)">1</div><span :class="labelClass(1)">DB 인증</span>
            </div>
            <div class="flex-1 h-0.5 mx-2" :class="barClass(1)"></div>
            <div class="flex items-center gap-3">
              <div :class="circleClass(2)">2</div><span :class="labelClass(2)">본인 인증</span>
            </div>
            <div class="flex-1 h-0.5 mx-2" :class="barClass(2)"></div>
            <div class="flex items-center gap-3">
              <div :class="circleClass(3)">3</div><span :class="labelClass(3)">회원 등록</span>
            </div>
          </div>
          <div class="mt-2 h-2 w-full bg-slate-200/70 rounded-full overflow-hidden">
            <div class="h-full bg-indigo-600 transition-all"
                 :style="{ width: step === 1 ? '33%' : step === 2 ? '67%' : '100%' }" />
          </div>
        </div>

        <!-- 본문 -->
        <div class="px-8 pb-8">
          <!-- STEP 1: DB 인증 (시뮬레이션) -->
          <div v-if="step === 1" class="space-y-4">
            <div class="space-y-3">
              <!-- 회원 구분 -->
              <div>
                <label class="block text-sm font-medium text-slate-700">회원 구분</label>
                <div class="mt-2 grid grid-cols-2 gap-2">
                  <button type="button"
                          class="px-3 py-2 rounded-xl border text-sm transition hover:bg-indigo-50"
                          :class="type === 0 ? 'border-indigo-600 text-indigo-700 bg-indigo-50' : 'border-slate-300 text-slate-700 bg-white'"
                          @click="type = 0">직원</button>
                  <button type="button"
                          class="px-3 py-2 rounded-xl border text-sm transition hover:bg-indigo-50"
                          :class="type === 1 ? 'border-indigo-600 text-indigo-700 bg-indigo-50' : 'border-slate-300 text-slate-700 bg-white'"
                          @click="type = 1">공선회</button>
                </div>
              </div>
              <!-- 이름 -->
              <div>
                <label class="block text-sm font-medium text-slate-700">이름</label>
                <input v-model.trim="name" type="text"
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                       placeholder="홍길동" />
              </div>
              <!-- 이메일 -->
              <div>
                <label class="block text-sm font-medium text-slate-700">이메일 (선택)</label>
                <input v-model.trim="email" type="email"
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                       placeholder="you@example.com" />
              </div>
              <!-- 전화번호 -->
              <div>
                <label class="block text-sm font-medium text-slate-700">전화번호 (선택)</label>
                <input v-model.trim="phone" type="tel"
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                       placeholder="010-1234-5678" />
              </div>
            </div>

            <p class="text-xs text-slate-500">※ 이메일/전화는 둘 중 하나만 입력하면 됩니다. (시뮬레이션)</p>

            <div class="flex items-center justify-end gap-2 pt-2">
              <button type="button"
                      class="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200"
                      @click="resetAll">초기화</button>
              <button type="button"
                      class="px-4 py-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
                      :disabled="!canVerifyBase"
                      @click="onVerifyBase">인증하기</button>
            </div>
          </div>

          <!-- STEP 2: 본인 인증 (시뮬레이션: 로컬 생성/검증) -->
          <div v-if="step === 2" class="space-y-4">
            <!-- 요약 표시 (비활성 필드) -->
            <div class="space-y-3">
              <div>
                <label class="block text-sm font-medium text-slate-700">회원 구분</label>
                <input :value="typeLabel" disabled
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-slate-600" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">이름</label>
                <input :value="name" disabled
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-slate-600" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">이메일</label>
                <input :value="email || '—'" disabled
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-slate-600" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">전화번호</label>
                <input :value="phone || '—'" disabled
                       class="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-slate-600" />
              </div>
            </div>

            <!-- 코드 전송 블록 -->
            <div class="rounded-2xl border border-indigo-200 bg-indigo-50/60 p-4">
              <div class="flex flex-wrap items-center gap-2">
                <button type="button"
                        class="px-3 py-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
                        :disabled="sending"
                        @click="onSendCode">인증번호 전송</button>
                <span class="text-sm text-slate-600" v-if="code">
                  시뮬레이션 코드: <b class="font-mono">{{ code }}</b>
                  <span v-if="remainingSec > 0" class="ml-2 text-xs text-slate-500">({{ remainLabel }} 남음)</span>
                </span>
              </div>
              <p class="mt-1 text-xs text-slate-500">※ 실제 발송 없이, 화면에 표시된 코드를 입력하면 됩니다.</p>
            </div>

            <!-- 인증번호 입력 (전화번호 입력과 동일한 너비 = 전체 폭) -->
            <div>
              <label class="block text-sm font-medium text-slate-700">인증번호 (5자리)</label>
              <input v-model.trim="codeInput" maxlength="5"
                     class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono tracking-widest"
                     placeholder="00000" />
            </div>

            <!-- 하단 우측 버튼: 이전 · 인증  -->
            <div class="pt-2 flex justify-end gap-2">
              <button type="button"
                      class="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200"
                      @click="backToStep1">이전</button>
              <button type="button"
                      class="px-4 py-2 rounded-xl bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-50"
                      :disabled="!code || codeInput.length !== 5"
                      @click="onVerifyAndNext">인증</button>
            </div>
          </div>

          <!-- STEP 3: 회원 등록 -->
          <div v-if="step === 3" class="space-y-4">
            <!-- 아이디 (한 행 + 우측 중복확인 버튼, 줄바꿈 방지) -->
            <div>
              <label class="block text-sm font-medium text-slate-700">아이디</label>
              <div class="mt-2 flex items-stretch gap-2">
                <input v-model.trim="memberId"
                       class="flex-1 min-w-0 rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                       placeholder="원하는 아이디" @keyup.enter="onCheckId" />
                <button type="button"
                        class="shrink-0 px-3 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 whitespace-nowrap"
                        @click="onCheckId">중복확인</button>
              </div>
              <p class="mt-1 text-xs"
                 :class="idAvailable === true ? 'text-emerald-600' : idAvailable === false ? 'text-rose-600' : 'text-slate-500'">
                {{ idMessage }}
              </p>
            </div>

            <!-- 비밀번호 (각각 한 행) -->
            <div>
              <label class="block text-sm font-medium text-slate-700">비밀번호</label>
              <input v-model="pass" type="password"
                     class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                     placeholder="8자 이상 권장" />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700">비밀번호 재입력</label>
              <input v-model="pass2" type="password"
                     class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                     placeholder="한 번 더" />
            </div>

            <!-- 요약 -->
            <div class="rounded-2xl border border-slate-200 bg-white/70 p-4">
              <h3 class="text-sm font-semibold text-slate-700">등록 요약</h3>
              <div class="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-slate-600">
                <div>구분: <b>{{ typeLabel }}</b></div>
                <div>이름: <b>{{ name }}</b></div>
                <div>이메일: <b>{{ email || '—' }}</b></div>
                <div>전화번호: <b>{{ phone || '—' }}</b></div>
              </div>
              <p class="mt-2 text-xs text-slate-500">※ 지금은 시뮬레이션 단계입니다. 실제 저장은 추후 백엔드 연동.</p>
            </div>

            <!-- 버튼: 이전 ⇢ 등록 (좌우 인접 배치) -->
            <div class="flex items-center justify-end gap-2 pt-2">
              <button type="button"
                      class="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200"
                      @click="step = 2">이전</button>
              <button type="button"
                      class="px-4 py-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
                      :disabled="!canSubmit"
                      @click="onSubmit">등록</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* D:\SmartApc\frontend\src\views\SignupView.vue */
import { ref, computed, onBeforeUnmount } from 'vue'
import { useRouter, RouterLink } from 'vue-router'

/* ===== 상태 ===== */
const step = ref(1)        // 1: DB 인증, 2: 본인인증, 3: 회원등록
const type = ref(0)        // 0: 직원, 1: 공선회
const name = ref('')
const email = ref('')
const phone = ref('')

// Step1 결과(시뮬레이션)
const refNo = ref(null)

// Step2: 시뮬레이션 전용 상태
const code        = ref('')     // 생성된 인증코드(로컬)
const codeInput   = ref('')     // 사용자가 입력
const sending     = ref(false)  // 전송 버튼 로딩
const verifiedCode= ref(false)  // 검증 성공 여부
const expiresAt   = ref(null)   // 만료시각(ms)
const remainingSec= ref(0)      // 남은 초
let otpTimer

// Step3: 회원 정보
const memberId = ref('')
const pass     = ref('')
const pass2    = ref('')
const idAvailable = ref(null) // true/false/null
const idMessage   = ref('아이디 중복 여부를 확인해 주세요.')

const router = useRouter()

/* ===== 계산 속성 ===== */
const typeLabel = computed(() => (type.value === 0 ? '직원' : '공선회'))
const canVerifyBase = computed(() => !!name.value && (!!email.value || !!phone.value))
const canSubmit = computed(() =>
  verifiedCode.value &&
  memberId.value.length >= 3 &&
  idAvailable.value === true &&
  pass.value.length >= 4 &&
  pass.value === pass2.value
)
const remainLabel = computed(() => {
  const s = Math.max(0, remainingSec.value | 0)
  const m = String(Math.floor(s / 60)).padStart(2, '0')
  const r = String(s % 60).padStart(2, '0')
  return `${m}:${r}`
})

/* ===== 스텝퍼 UI 헬퍼 ===== */
function circleClass(n){return step.value >= n
  ? 'h-8 w-8 rounded-full flex items-center justify-center bg-indigo-600 text-white font-bold'
  : 'h-8 w-8 rounded-full flex items-center justify-center bg-slate-200 text-slate-600 font-bold'}
function labelClass(n){return step.value >= n
  ? 'text-indigo-700 text-sm font-semibold'
  : 'text-slate-400 text-sm font-semibold'}
function barClass(n){return step.value > n ? 'bg-indigo-600' : 'bg-slate-200'}

/* ===== 유틸 ===== */
function resetAll(){
  step.value = 1
  type.value = 0
  name.value = ''; email.value = ''; phone.value = ''
  refNo.value = null
  code.value = ''; codeInput.value = ''; sending.value = false
  verifiedCode.value = false; clearOtpTimer(); expiresAt.value = null; remainingSec.value = 0
  memberId.value = ''; pass.value = ''; pass2.value = ''
  idAvailable.value = null; idMessage.value = '아이디 중복 여부를 확인해 주세요.'
}
function backToStep1(){
  verifiedCode.value = false
  code.value = ''; codeInput.value = ''; clearOtpTimer(); remainingSec.value = 0; expiresAt.value = null
  step.value = 1
}
function clearOtpTimer(){
  if (otpTimer){ clearInterval(otpTimer); otpTimer = undefined }
}
onBeforeUnmount(() => clearOtpTimer())

/* ===== STEP 1: DB 인증 (시뮬레이션) ===== */
function onVerifyBase(){
  if (!canVerifyBase.value) return
  refNo.value = Math.floor(Math.random() * 100000) + 1
  alert('DB 인증 성공(시뮬레이션)!')
  step.value = 2
}

/* ===== STEP 2: 인증번호 전송/검증 (시뮬레이션) ===== */
async function onSendCode(){
  if (!email.value && !phone.value){
    alert('이메일 또는 전화번호를 입력해 주세요.')
    return
  }
  sending.value = true
  try{
    code.value = Math.floor(Math.random() * 100000).toString().padStart(5, '0') // 00000~99999
    expiresAt.value = Date.now() + 5 * 60 * 1000
    remainingSec.value = 5 * 60
    clearOtpTimer()
    otpTimer = window.setInterval(() => {
      const left = Math.max(0, Math.floor(((expiresAt.value ?? 0) - Date.now()) / 1000))
      remainingSec.value = left
      if (left <= 0) clearOtpTimer()
    }, 1000)
  } finally {
    sending.value = false
  }
}
function onVerifyAndNext(){
  if (!code.value){ alert('먼저 인증번호를 전송해 주세요.'); return }
  if ((expiresAt.value ?? 0) < Date.now()){ alert('인증번호가 만료되었습니다. 다시 전송해 주세요.'); return }
  verifiedCode.value = codeInput.value.trim() === code.value
  if (!verifiedCode.value){
    alert('인증번호가 일치하지 않습니다.')
  } else {
    clearOtpTimer()
    // 인증 성공 시, 즉시 3단계로 전환
    step.value = 3
  }
}

/* ===== STEP 3: 아이디 중복확인/등록 (시뮬레이션) ===== */
function onCheckId(){
  const v = memberId.value.trim().toLowerCase()
  if (!v){ idAvailable.value = null; idMessage.value = '아이디를 입력해 주세요.'; return }
  const banned = ['admin','test','root']
  if (banned.includes(v)){ idAvailable.value = false; idMessage.value = '이미 사용 중인 아이디입니다.' }
  else { idAvailable.value = true; idMessage.value = '사용 가능한 아이디입니다.' }
}
function onSubmit(){
  if (!canSubmit.value){ alert('입력 정보를 확인해 주세요.'); return }
  if (pass.value !== pass2.value){ alert('비밀번호가 일치하지 않습니다.'); return }
  alert('회원등록이 완료되었습니다! (시뮬레이션)\n이제 로그인 화면으로 이동합니다.')
  router.push('/login')
}
</script>

<style scoped>
/* 필요 시 추가 커스텀 스타일 */
</style>
