<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">{{ $t('nav.submissions') }}</h1>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <template v-else>
      <!-- 申請・書類 -->
      <div class="card mb-6">
        <h2 class="text-sand font-semibold mb-4">提出が必要なもの</h2>
        <ul class="space-y-3">
          <li v-for="s in submissions" :key="s.id"
            class="flex items-center justify-between text-sm border-b border-navy-800 pb-3 last:border-0">
            <div>
              <p :class="s.status === 'pending' ? 'text-sand' : 'text-sand/50'">{{ s.title_ja }}</p>
              <p v-if="s.due_date" class="text-sand/40 text-xs mt-0.5">締切 {{ s.due_date }}</p>
            </div>
            <div class="flex items-center gap-2">
              <span :class="statusClass(s.status)" class="text-xs px-2 py-0.5 rounded font-semibold">
                {{ statusLabel(s.status) }}
              </span>
              <button v-if="s.status === 'pending'" @click="handleSubmit(s)"
                class="btn-primary text-xs py-1 px-3">
                提出
              </button>
            </div>
          </li>
        </ul>
      </div>

      <!-- アンケート -->
      <div class="card">
        <h2 class="text-sand font-semibold mb-4">アンケート</h2>
        <div v-for="survey in surveys" :key="survey.id" class="mb-6 last:mb-0">
          <p class="text-sand text-sm font-medium mb-3">{{ survey.title_ja }}</p>
          <div v-if="survey.my_response !== null" class="text-teal-400 text-sm">
            ✓ ご回答ありがとうございました（{{ survey.options_ja[survey.my_response] }}）
          </div>
          <div v-else class="space-y-2">
            <button v-for="(opt, idx) in survey.options_ja" :key="idx"
              @click="handleSurvey(survey, idx)"
              class="block w-full text-left text-sm text-sand/70 hover:text-sand bg-navy-800 hover:bg-navy-700 px-4 py-2 rounded-lg transition-colors">
              {{ opt }}
            </button>
          </div>
        </div>
        <p v-if="!surveys.length" class="text-sand/40 text-sm">現在アンケートはありません</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSubmissions, submitSubmission, getSurveys, answerSurvey } from '@/api/parent'

const submissions = ref([])
const surveys = ref([])
const loading = ref(true)

const statusMap = { pending: '提出待ち', submitted: '提出済', accepted: '受理済' }
const statusColorMap = { pending: 'bg-yellow-500/20 text-yellow-400', submitted: 'bg-teal-600/20 text-teal-400', accepted: 'bg-teal-600/30 text-teal-300' }

function statusLabel(s) { return statusMap[s] || s }
function statusClass(s) { return statusColorMap[s] || '' }

async function handleSubmit(sub) {
  await submitSubmission(sub.id)
  sub.status = 'submitted'
}

async function handleSurvey(survey, idx) {
  await answerSurvey(survey.id, idx)
  survey.my_response = idx
}

onMounted(async () => {
  try {
    const [s, sv] = await Promise.all([getSubmissions(), getSurveys()])
    submissions.value = s.data
    surveys.value = sv.data
  } finally {
    loading.value = false
  }
})
</script>
