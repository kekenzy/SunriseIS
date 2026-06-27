import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDashboard } from '@/api/parent'

export const useDashboardStore = defineStore('dashboard', () => {
  const data = ref(null)
  const loading = ref(false)

  async function fetchDashboard() {
    loading.value = true
    try {
      const res = await getDashboard()
      data.value = res.data
    } finally {
      loading.value = false
    }
  }

  return { data, loading, fetchDashboard }
})
