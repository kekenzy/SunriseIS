<template>
  <div class="p-6 max-w-5xl mx-auto">
    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>
    <template v-else-if="data">
      <!-- Greeting -->
      <h1 class="text-2xl font-bold text-sand mb-2">
        {{ $t('dashboard.greeting', { name: data.parent_name }) }} 👋
      </h1>
      <p v-if="data.children?.[0]" class="text-sand/50 text-sm mb-8">
        {{ data.children[0].name_ja }} さんの最新情報です。
      </p>

      <!-- Summary Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <SummaryCard icon="💴" :label="$t('dashboard.nextPayment')" value="¥48,000" sub="6/30 期日" />
        <SummaryCard icon="📅" :label="$t('dashboard.attendance')"
          :value="`${data.attendance?.present ?? 0} / ${data.attendance?.total ?? 0}日`"
          :sub="`出席率 ${data.attendance?.rate ?? 0}%`" />
        <SummaryCard icon="🔔" :label="$t('dashboard.unreadNotices')"
          :value="`${data.unread_notices ?? 0}${$t('common.items')}`"
          @click="$router.push({ name: 'parent-notices' })" clickable />
        <SummaryCard icon="🎉" :label="$t('dashboard.upcomingEvents')"
          :value="data.upcoming_events?.[0]?.title_ja ?? '-'"
          :sub="data.upcoming_events?.[0]?.event_date ?? ''" />
      </div>

      <!-- Upcoming Events -->
      <div class="card mb-6" v-if="data.upcoming_events?.length">
        <h2 class="text-sand font-semibold mb-4">{{ $t('dashboard.upcomingEvents') }}</h2>
        <ul class="space-y-3">
          <li v-for="ev in data.upcoming_events" :key="ev.id"
            class="flex items-center justify-between text-sm text-sand/80 border-b border-navy-800 pb-2 last:border-0">
            <span>{{ ev.title_ja }}</span>
            <span class="text-teal-600 font-medium">{{ ev.event_date }}</span>
          </li>
        </ul>
      </div>

      <!-- Recent Notices -->
      <div class="card" v-if="notices.length">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-sand font-semibold">{{ $t('notices.title') }}</h2>
          <RouterLink to="/portal/notices" class="text-teal-600 text-sm hover:underline">{{ $t('dashboard.viewAll') }}</RouterLink>
        </div>
        <ul class="space-y-3">
          <li v-for="n in notices.slice(0, 3)" :key="n.id"
            class="flex items-start justify-between text-sm border-b border-navy-800 pb-2 last:border-0">
            <div class="flex items-center gap-2">
              <span v-if="n.is_important" class="text-red-400 text-xs font-bold">重要</span>
              <span :class="n.is_read ? 'text-sand/50' : 'text-sand'">{{ n.title_ja }}</span>
            </div>
            <span class="text-sand/40 text-xs shrink-0 ml-2">{{ n.published_at?.slice(0, 10) }}</span>
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useDashboardStore } from '@/stores/dashboard'
import { useNoticesStore } from '@/stores/notices'
import SummaryCard from '@/components/dashboard/SummaryCard.vue'

const dashStore = useDashboardStore()
const noticesStore = useNoticesStore()
const { data, loading } = storeToRefs(dashStore)
const { notices } = storeToRefs(noticesStore)

onMounted(async () => {
  await Promise.all([dashStore.fetchDashboard(), noticesStore.fetchNotices()])
})
</script>
