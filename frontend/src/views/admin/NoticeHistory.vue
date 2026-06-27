<template>
  <div class="p-6 max-w-4xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-sand">{{ $t('admin.history') }}</h1>
      <RouterLink to="/admin/notices/compose" class="btn-primary text-sm">
        + {{ $t('admin.compose') }}
      </RouterLink>
    </div>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <ul v-else class="space-y-3">
      <li v-for="n in notices" :key="n.id" class="card">
        <div class="flex justify-between items-start gap-3">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span v-if="n.is_important" class="bg-red-500/20 text-red-400 text-xs font-bold px-2 py-0.5 rounded">重要</span>
              <span class="text-sand font-medium text-sm">{{ n.title_ja }}</span>
            </div>
            <p class="text-sand/50 text-xs">{{ n.published_at?.slice(0, 10) }} · 対象: {{ targetLabel(n.target_role) }}</p>
          </div>
          <button @click="handleDelete(n.id)" class="text-red-400/60 hover:text-red-400 text-xs shrink-0">削除</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { getAdminNotices, deleteNotice } from '@/api/admin'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const notices = ref([])
const loading = ref(true)

const targetMap = { all: '全員', parent: '保護者', admin: '管理者・教職員' }
function targetLabel(role) { return targetMap[role] || role }

async function load() {
  loading.value = true
  try {
    const { data } = await getAdminNotices()
    notices.value = data
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('このお知らせを削除しますか？')) return
  await deleteNotice(id)
  notices.value = notices.value.filter(n => n.id !== id)
}

onMounted(load)
</script>
