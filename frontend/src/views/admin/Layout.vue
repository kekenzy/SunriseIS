<template>
  <div class="min-h-screen bg-navy-950 flex">
    <aside class="w-56 bg-navy-900 hidden md:flex flex-col py-6 px-3 shrink-0">
      <div class="flex items-center gap-2 px-3 mb-8">
        <div class="w-8 h-8 bg-teal-600 rounded-full flex items-center justify-center text-white text-sm font-bold">A</div>
        <span class="text-sand text-sm font-semibold">Admin Console</span>
      </div>
      <nav class="flex-1 space-y-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-sand/70 hover:text-sand hover:bg-navy-800 transition-colors"
          active-class="bg-navy-800 text-sand"
        >
          <span>{{ item.icon }}</span>
          <span>{{ $t(item.label) }}</span>
        </RouterLink>
      </nav>
      <div class="pt-4 border-t border-navy-800">
        <button @click="handleLogout" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-sand/50 hover:text-sand hover:bg-navy-800 transition-colors w-full">
          <span>🚪</span><span>{{ $t('nav.logout') }}</span>
        </button>
      </div>
    </aside>
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { to: '/admin', icon: '📊', label: 'nav.home' },
  { to: '/admin/notices', icon: '📢', label: 'nav.notices' },
  { to: '/admin/students', icon: '👦', label: 'nav.students' },
  { to: '/admin/bills', icon: '💴', label: 'nav.payment' },
]

async function handleLogout() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>
