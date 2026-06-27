<template>
  <div class="min-h-screen bg-navy-950 flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-14 h-14 bg-teal-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">S</div>
        <p class="text-sand/60 text-sm">Sunrise International School</p>
      </div>

      <!-- Card -->
      <div class="card">
        <!-- Tabs -->
        <div class="flex bg-navy-800 rounded-lg p-1 mb-6">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            @click="activeTab = tab.value"
            :class="['flex-1 py-2 rounded-md text-sm font-medium transition-colors', activeTab === tab.value ? 'bg-teal-600 text-white' : 'text-sand/60 hover:text-sand']"
          >
            {{ $t(`login.${tab.value}`) }}
          </button>
        </div>

        <h2 class="text-xl font-bold text-sand mb-6">{{ $t('login.title') }}</h2>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm text-sand/70 mb-1">{{ $t('login.email') }}</label>
            <input v-model="form.email" type="email" required class="input-field" autocomplete="email" />
          </div>
          <div>
            <label class="block text-sm text-sand/70 mb-1">{{ $t('login.password') }}</label>
            <input v-model="form.password" type="password" required class="input-field" autocomplete="current-password" />
          </div>

          <p v-if="error" class="text-red-400 text-sm">{{ $t('login.error') }}</p>

          <button type="submit" :disabled="loading" class="btn-primary w-full mt-2">
            {{ loading ? $t('common.loading') : $t('login.submit') }}
          </button>
        </form>
      </div>

      <!-- Lang toggle -->
      <div class="text-center mt-6">
        <button @click="toggleLang" class="text-sand/40 hover:text-sand text-sm transition-colors">
          {{ locale === 'ja' ? 'Switch to English' : '日本語に切り替え' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { locale } = useI18n()
const router = useRouter()
const auth = useAuthStore()

const activeTab = ref('parent')
const tabs = [{ value: 'parent' }, { value: 'admin' }]
const form = reactive({ email: '', password: '' })
const loading = ref(false)
const error = ref(false)

function toggleLang() {
  locale.value = locale.value === 'ja' ? 'en' : 'ja'
  localStorage.setItem('lang', locale.value)
}

async function handleLogin() {
  loading.value = true
  error.value = false
  try {
    await auth.login(form.email, form.password)
    if (auth.isAdmin) router.push({ name: 'admin-dashboard' })
    else router.push({ name: 'parent-dashboard' })
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}
</script>
