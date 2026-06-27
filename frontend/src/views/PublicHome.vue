<template>
  <div class="min-h-screen bg-[#F5F2EC] text-gray-800">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-teal-600 rounded-full flex items-center justify-center text-white font-bold text-sm">S</div>
          <span class="font-semibold text-gray-900">{{ $t('public.schoolName') }}</span>
        </div>
        <nav class="hidden md:flex items-center gap-6 text-sm text-gray-600">
          <a href="#" class="hover:text-teal-700">{{ $t('public.about') }}</a>
          <a href="#" class="hover:text-teal-700">{{ $t('public.programs') }}</a>
          <a href="#" class="hover:text-teal-700">{{ $t('public.admissions') }}</a>
          <a href="#" class="hover:text-teal-700">{{ $t('public.access') }}</a>
        </nav>
        <div class="flex items-center gap-3">
          <button @click="toggleLang" class="text-sm text-gray-500 hover:text-teal-700 font-medium">
            {{ locale === 'ja' ? 'EN' : 'JA' }}
          </button>
          <RouterLink to="/login" class="bg-teal-700 hover:bg-teal-800 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors">
            {{ $t('public.loginBtn') }}
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="bg-gradient-to-br from-teal-700 to-teal-900 text-white py-24 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <p class="text-teal-200 text-sm font-semibold tracking-widest uppercase mb-4">Sunrise International School</p>
        <h1 class="text-4xl md:text-5xl font-bold leading-tight mb-6">{{ $t('public.tagline') }}</h1>
        <RouterLink to="/login" class="inline-block bg-white text-teal-800 font-bold px-8 py-3 rounded-full hover:bg-teal-50 transition-colors mt-4">
          {{ $t('public.parentPortal') }} →
        </RouterLink>
      </div>
    </section>

    <!-- Programs -->
    <section class="py-16 px-4 max-w-6xl mx-auto">
      <h2 class="text-2xl font-bold text-center mb-10 text-gray-800">OUR PROGRAMS</h2>
      <div class="grid md:grid-cols-3 gap-6">
        <div v-for="p in programs" :key="p.icon" class="bg-white rounded-xl p-6 shadow-sm text-center">
          <div class="text-4xl mb-3">{{ p.icon }}</div>
          <h3 class="font-bold text-gray-900 mb-2">{{ p.title }}</h3>
          <p class="text-gray-500 text-sm">{{ p.body }}</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 py-10 px-4 text-sm">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between gap-6">
        <div>
          <p class="font-semibold text-white mb-2">Sunrise International School</p>
          <p>TEL 00-0000-0000</p>
        </div>
        <div class="flex gap-8">
          <div>
            <p class="text-white font-semibold mb-2">PORTAL</p>
            <RouterLink to="/login" class="block hover:text-white">{{ $t('public.parentPortal') }}</RouterLink>
          </div>
        </div>
      </div>
      <p class="text-center mt-8 text-gray-600">© 2026 Sunrise International School</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

function toggleLang() {
  locale.value = locale.value === 'ja' ? 'en' : 'ja'
  localStorage.setItem('lang', locale.value)
}

const programs = computed(() => [
  { icon: '🌏', title: locale.value === 'ja' ? 'インターナショナル教育' : 'International Education', body: locale.value === 'ja' ? '英語イマージョン環境で世界基準の教育を提供' : 'World-class education in an English immersion environment' },
  { icon: '🎨', title: locale.value === 'ja' ? '創造的学習' : 'Creative Learning', body: locale.value === 'ja' ? '芸術・音楽・体育を通じた全人教育' : 'Holistic education through arts, music, and physical education' },
  { icon: '🤝', title: locale.value === 'ja' ? 'コミュニティ' : 'Community', body: locale.value === 'ja' ? '保護者と学校が連携した温かいコミュニティ' : 'A warm community connecting parents and school' },
])
</script>
