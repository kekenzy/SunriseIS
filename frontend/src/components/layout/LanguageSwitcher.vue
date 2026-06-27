<template>
  <button @click="toggle" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-sand/50 hover:text-sand hover:bg-navy-800 transition-colors w-full">
    <span>🌐</span>
    <span>{{ locale === 'ja' ? 'English' : '日本語' }}</span>
  </button>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

function toggle() {
  locale.value = locale.value === 'ja' ? 'en' : 'ja'
  localStorage.setItem('lang', locale.value)
}
</script>
