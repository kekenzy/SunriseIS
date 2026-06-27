import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getNotices, getNotice } from '@/api/parent'

export const useNoticesStore = defineStore('notices', () => {
  const notices = ref([])
  const loading = ref(false)

  const unreadCount = computed(() => notices.value.filter(n => !n.is_read).length)

  async function fetchNotices() {
    loading.value = true
    try {
      const { data } = await getNotices()
      notices.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchNotice(id) {
    const { data } = await getNotice(id)
    const idx = notices.value.findIndex(n => n.id === id)
    if (idx !== -1) notices.value[idx] = data
    return data
  }

  return { notices, loading, unreadCount, fetchNotices, fetchNotice }
})
