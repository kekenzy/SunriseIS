import api from './index'

export const login = (email, password) =>
  api.post('/api/auth/login/', { email, password })

export const logout = (refresh) =>
  api.post('/api/auth/logout/', { refresh })

export const getMe = () =>
  api.get('/api/auth/me/')
