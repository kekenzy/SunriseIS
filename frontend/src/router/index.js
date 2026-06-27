import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/PublicHome.vue'), meta: { public: true } },
  { path: '/login', name: 'login', component: () => import('@/views/Login.vue'), meta: { public: true } },
  {
    path: '/portal',
    component: () => import('@/views/parent/Layout.vue'),
    meta: { requiresAuth: true, role: 'parent' },
    children: [
      { path: '', name: 'parent-dashboard', component: () => import('@/views/parent/Dashboard.vue') },
      { path: 'notices', name: 'parent-notices', component: () => import('@/views/parent/NoticeList.vue') },
      { path: 'notices/:id', name: 'parent-notice-detail', component: () => import('@/views/parent/NoticeDetail.vue') },
      { path: 'bills', name: 'parent-bills', component: () => import('@/views/parent/BillList.vue') },
      { path: 'attendance', name: 'parent-attendance', component: () => import('@/views/parent/AttendanceCalendar.vue') },
      { path: 'events', name: 'parent-events', component: () => import('@/views/parent/EventList.vue') },
      { path: 'submissions', name: 'parent-submissions', component: () => import('@/views/parent/SubmissionList.vue') },
    ]
  },
  {
    path: '/admin',
    component: () => import('@/views/admin/Layout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'notices', name: 'admin-notices', component: () => import('@/views/admin/NoticeHistory.vue') },
      { path: 'notices/compose', name: 'admin-notice-compose', component: () => import('@/views/admin/NoticeCompose.vue') },
      { path: 'students', name: 'admin-students', component: () => import('@/views/admin/StudentList.vue') },
      { path: 'bills', name: 'admin-bills', component: () => import('@/views/admin/BillList.vue') },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (to.meta.public) return true

  if (!auth.isAuthenticated) return { name: 'login' }

  if (!auth.user) {
    try { await auth.fetchMe() } catch { return { name: 'login' } }
  }

  if (to.meta.role === 'admin' && !auth.isAdmin) return { name: 'parent-dashboard' }
  if (to.meta.role === 'parent' && auth.isAdmin) return { name: 'admin-dashboard' }

  return true
})

export default router
