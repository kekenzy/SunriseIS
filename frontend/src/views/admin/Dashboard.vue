<template>
  <div class="p-6 max-w-5xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-8">{{ $t('admin.title') }}</h1>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <template v-else-if="data">
      <!-- Summary Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <SummaryCard icon="👦" :label="$t('admin.totalChildren')"
          :value="`${data.total_children}${$t('common.persons')}`" />
        <SummaryCard icon="✅" :label="$t('admin.presentToday')"
          :value="`${data.today_attendance?.present ?? 0}${$t('common.persons')}`" />
        <SummaryCard icon="❌" :label="$t('admin.absentToday')"
          :value="`${data.today_attendance?.absent ?? 0}${$t('common.persons')}`" />
        <SummaryCard icon="❓" :label="$t('admin.notRecorded')"
          :value="`${data.today_attendance?.not_recorded ?? 0}${$t('common.persons')}`" />
      </div>

      <!-- Quick compose -->
      <div class="card mb-6">
        <h2 class="text-sand font-semibold mb-3">クイック配信</h2>
        <p class="text-sand/50 text-sm mb-4">お知らせをすぐに配信できます。</p>
        <RouterLink to="/admin/notices/compose" class="btn-primary inline-block text-sm">
          {{ $t('admin.compose') }} →
        </RouterLink>
      </div>

      <!-- Stats -->
      <div class="card">
        <h2 class="text-sand font-semibold mb-3">{{ $t('admin.totalNotices') }}</h2>
        <p class="text-4xl font-bold text-teal-600">{{ data.total_notices }}</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { getAdminDashboard } from '@/api/admin'
import SummaryCard from '@/components/dashboard/SummaryCard.vue'

const data = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getAdminDashboard()
    data.value = res.data
  } finally {
    loading.value = false
  }
})
</script>
