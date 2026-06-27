<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">{{ $t('nav.attendance') }}</h1>

    <!-- 月切替 -->
    <div class="flex items-center gap-4 mb-6">
      <button @click="changeMonth(-1)" class="btn-ghost px-3 py-1 text-sm">←</button>
      <span class="text-sand font-semibold">{{ year }}年 {{ month }}月</span>
      <button @click="changeMonth(1)" class="btn-ghost px-3 py-1 text-sm">→</button>
    </div>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <template v-else>
      <!-- サマリー -->
      <div class="flex gap-4 text-sm mb-6">
        <span class="text-teal-400">出席 {{ presentCount }}</span>
        <span class="text-red-400">欠席 {{ absentCount }}</span>
        <span class="text-yellow-400">行事 {{ eventCount }}</span>
      </div>

      <!-- カレンダー -->
      <div class="card mb-6">
        <div class="grid grid-cols-7 gap-1 text-center text-xs text-sand/40 mb-2">
          <span v-for="d in ['日','月','火','水','木','金','土']" :key="d">{{ d }}</span>
        </div>
        <div class="grid grid-cols-7 gap-1">
          <span v-for="_ in firstDayOffset" :key="'e'+_"></span>
          <div v-for="day in daysInMonth" :key="day"
            :class="['text-center py-1.5 rounded text-xs', cellClass(day)]">
            {{ day }}
          </div>
        </div>
      </div>

      <!-- 欠席連絡 -->
      <div class="card">
        <h2 class="text-sand font-semibold mb-4">欠席・遅刻を連絡する</h2>
        <form @submit.prevent="handleAbsence" class="space-y-3">
          <div>
            <label class="block text-sm text-sand/60 mb-1">日付</label>
            <input v-model="absenceForm.date" type="date" required class="input-field" />
          </div>
          <div>
            <label class="block text-sm text-sand/60 mb-1">理由（任意）</label>
            <textarea v-model="absenceForm.reason" rows="3" class="input-field resize-none"></textarea>
          </div>
          <p v-if="absenceSuccess" class="text-teal-400 text-sm">連絡しました ✓</p>
          <button type="submit" :disabled="absenceLoading" class="btn-primary text-sm">
            {{ absenceLoading ? '送信中…' : '連絡フォームを送信' }}
          </button>
        </form>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getAttendance, postAbsence } from '@/api/parent'

const today = new Date()
const year = ref(today.getFullYear())
const month = ref(today.getMonth() + 1)
const records = ref([])
const loading = ref(true)
const absenceForm = ref({ date: '', reason: '' })
const absenceLoading = ref(false)
const absenceSuccess = ref(false)

const statusMap = computed(() => {
  const m = {}
  records.value.forEach(r => {
    m[Number(r.date.split('-')[2])] = r.status
  })
  return m
})

const presentCount = computed(() => records.value.filter(r => r.status === 'present').length)
const absentCount = computed(() => records.value.filter(r => r.status === 'absent').length)
const eventCount = computed(() => records.value.filter(r => r.status === 'event').length)

const daysInMonth = computed(() => new Date(year.value, month.value, 0).getDate())
const firstDayOffset = computed(() => new Date(year.value, month.value - 1, 1).getDay())

function cellClass(day) {
  const s = statusMap.value[day]
  if (!s) return 'text-sand/30'
  if (s === 'present') return 'bg-teal-600/20 text-teal-400'
  if (s === 'absent') return 'bg-red-500/20 text-red-400'
  if (s === 'event') return 'bg-yellow-500/20 text-yellow-400'
  return ''
}

async function load() {
  loading.value = true
  try {
    const { data } = await getAttendance(year.value, month.value)
    records.value = data.records || []
  } finally {
    loading.value = false
  }
}

async function changeMonth(delta) {
  month.value += delta
  if (month.value > 12) { month.value = 1; year.value++ }
  if (month.value < 1) { month.value = 12; year.value-- }
  await load()
}

async function handleAbsence() {
  absenceLoading.value = true
  absenceSuccess.value = false
  try {
    await postAbsence(absenceForm.value)
    absenceSuccess.value = true
    absenceForm.value = { date: '', reason: '' }
    await load()
  } finally {
    absenceLoading.value = false
  }
}

onMounted(load)
</script>
