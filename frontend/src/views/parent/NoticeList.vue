<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">{{ $t('notices.title') }}</h1>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <div v-else-if="!notices.length" class="text-sand/40 text-center py-20">
      {{ $t('notices.noNotices') }}
    </div>

    <ul v-else class="space-y-3">
      <li v-for="n in notices" :key="n.id">
        <RouterLink :to="`/portal/notices/${n.id}`"
          class="card block hover:bg-navy-800 transition-colors cursor-pointer">
          <div class="flex items-start justify-between gap-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span v-if="n.is_important"
                class="bg-red-500/20 text-red-400 text-xs font-bold px-2 py-0.5 rounded">
                {{ $t('notices.important') }}
              </span>
              <span v-if="!n.is_read"
                class="bg-teal-600/20 text-teal-400 text-xs px-2 py-0.5 rounded">
                {{ $t('notices.unread') }}
              </span>
              <span :class="['font-medium text-sm', n.is_read ? 'text-sand/60' : 'text-sand']">
                {{ n.title_ja }}
              </span>
            </div>
            <span class="text-sand/40 text-xs shrink-0">{{ n.published_at?.slice(0, 10) }}</span>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useNoticesStore } from '@/stores/notices'

const store = useNoticesStore()
const { notices, loading } = storeToRefs(store)

onMounted(() => store.fetchNotices())
</script>
