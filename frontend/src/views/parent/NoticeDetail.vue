<template>
  <div class="p-6 max-w-3xl mx-auto">
    <RouterLink to="/portal/notices" class="text-teal-600 text-sm hover:underline mb-6 block">
      ← {{ $t('common.back') }}
    </RouterLink>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <div v-else-if="notice" class="card">
      <div class="flex items-center gap-2 mb-2">
        <span v-if="notice.is_important"
          class="bg-red-500/20 text-red-400 text-xs font-bold px-2 py-0.5 rounded">
          {{ $t('notices.important') }}
        </span>
        <span class="text-sand/40 text-xs">{{ notice.published_at?.slice(0, 10) }}</span>
      </div>
      <h1 class="text-xl font-bold text-sand mb-6">{{ notice.title_ja }}</h1>
      <p class="text-sand/80 leading-relaxed whitespace-pre-wrap">{{ notice.body_ja }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useNoticesStore } from '@/stores/notices'

const route = useRoute()
const store = useNoticesStore()
const notice = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    notice.value = await store.fetchNotice(Number(route.params.id))
  } finally {
    loading.value = false
  }
})
</script>
