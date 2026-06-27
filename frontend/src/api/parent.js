import api from './index'

export const getDashboard = () => api.get('/api/parent/dashboard/')
export const getNotices = () => api.get('/api/parent/notices/')
export const getNotice = (id) => api.get(`/api/parent/notices/${id}/`)
export const getChildren = () => api.get('/api/parent/children/')
export const getAttendance = (year, month) =>
  api.get('/api/parent/attendance/', { params: { year, month } })
export const getEvents = () => api.get('/api/parent/events/')
export const postRsvp = (eventId, status) =>
  api.post(`/api/parent/events/${eventId}/rsvp/`, { status })
export const getBills = () => api.get('/api/parent/bills/')
export const payBill = (id) => api.post(`/api/parent/bills/${id}/pay/`)
export const getReceipt = (id) => api.get(`/api/parent/bills/${id}/receipt/`)
export const postAbsence = (data) => api.post('/api/parent/absence/', data)
export const getSubmissions = () => api.get('/api/parent/submissions/')
export const submitSubmission = (id) => api.post(`/api/parent/submissions/${id}/submit/`)
export const getSurveys = () => api.get('/api/parent/surveys/')
export const answerSurvey = (id, choice_index) =>
  api.post(`/api/parent/surveys/${id}/answer/`, { choice_index })
