import api from './index'

export const getAdminDashboard = () => api.get('/api/admin/dashboard/')
export const getAdminNotices = () => api.get('/api/admin/notices/')
export const createNotice = (data) => api.post('/api/admin/notices/', data)
export const updateNotice = (id, data) => api.patch(`/api/admin/notices/${id}/`, data)
export const deleteNotice = (id) => api.delete(`/api/admin/notices/${id}/`)
export const getAdminBills = () => api.get('/api/admin/bills/')
export const getAdminStudents = (q) => api.get('/api/admin/students/', { params: q ? { q } : {} })
