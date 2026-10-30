import axios from 'axios'

// 本番は nginx の /api/ 経由（同一オリジン）で呼ぶ。backend の 8000 番は外部に公開していない
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? (import.meta.env.DEV ? 'http://localhost:8000' : ''),
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let refreshing = null

// refresh はローテーションで使い捨てになるため、同時に401になったリクエストの更新は1回にまとめる
function refreshAccessToken() {
  if (!refreshing) {
    const refresh = localStorage.getItem('refresh_token')
    refreshing = (async () => {
      try {
        const { data } = await axios.post('/api/auth/token/refresh/', { refresh })
        localStorage.setItem('access_token', data.access)
        if (data.refresh) localStorage.setItem('refresh_token', data.refresh)
        return data.access
      } catch (e) {
        // 別タブが先に更新していれば、そのトークンを使う
        const access = localStorage.getItem('access_token')
        if (access && localStorage.getItem('refresh_token') !== refresh) return access
        throw e
      }
    })().finally(() => {
      refreshing = null
    })
  }
  return refreshing
}

api.interceptors.response.use(
  res => res,
  async error => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const access = await refreshAccessToken()
          original.headers.Authorization = `Bearer ${access}`
          return api(original)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
