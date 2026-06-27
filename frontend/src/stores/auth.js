import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, logout as apiLogout, getMe } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'staff')
  const isParent = computed(() => user.value?.role === 'parent')

  async function login(email, password) {
    const { data } = await apiLogin(email, password)
    accessToken.value = data.access
    refreshToken.value = data.refresh
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    await fetchMe()
  }

  async function fetchMe() {
    const { data } = await getMe()
    user.value = data
  }

  async function logout() {
    try {
      if (refreshToken.value) await apiLogout(refreshToken.value)
    } finally {
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  return { user, accessToken, isAuthenticated, isAdmin, isParent, login, logout, fetchMe }
})
