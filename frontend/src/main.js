import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import ja from './i18n/ja.json'
import en from './i18n/en.json'
import './style.css'

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('lang') || 'ja',
  fallbackLocale: 'ja',
  messages: { ja, en }
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
