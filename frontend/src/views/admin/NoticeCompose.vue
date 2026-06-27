<template>
  <div class="p-6 max-w-2xl mx-auto">
    <RouterLink to="/admin/notices" class="text-teal-600 text-sm hover:underline mb-6 block">
      ← {{ $t('common.back') }}
    </RouterLink>
    <h1 class="text-2xl font-bold text-sand mb-6">{{ $t('admin.compose') }}</h1>

    <div class="card">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm text-sand/70 mb-1">{{ $t('admin.composeTitle') }}</label>
          <input v-model="form.title_ja" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm text-sand/70 mb-1">{{ $t('admin.composeTitleEn') }}</label>
          <input v-model="form.title_en" class="input-field" />
        </div>
        <div>
          <label class="block text-sm text-sand/70 mb-1">{{ $t('admin.composeBody') }}</label>
          <textarea v-model="form.body_ja" required rows="4" class="input-field resize-none"></textarea>
        </div>
        <div>
          <label class="block text-sm text-sand/70 mb-1">{{ $t('admin.composeBodyEn') }}</label>
          <textarea v-model="form.body_en" rows="4" class="input-field resize-none"></textarea>
        </div>
        <div>
          <label class="block text-sm text-sand/70 mb-1">{{ $t('admin.target') }}</label>
          <select v-model="form.target_role" class="input-field">
            <option value="all">{{ $t('admin.targetAll') }}</option>
            <option value="parent">{{ $t('admin.targetParent') }}</option>
            <option value="admin">{{ $t('admin.targetAdmin') }}</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <input id="important" type="checkbox" v-model="form.is_important" class="accent-teal-600" />
          <label for="important" class="text-sm text-sand/70">{{ $t('admin.important') }}</label>
        </div>

        <p v-if="success" class="text-teal-400 text-sm">配信しました ✓</p>
        <p v-if="error" class="text-red-400 text-sm">{{ $t('common.error') }}</p>

        <button type="submit" :disabled="loading" class="btn-primary w-full">
          {{ loading ? $t('common.loading') : $t('admin.send') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { createNotice } from '@/api/admin'

const router = useRouter()
const loading = ref(false)
const success = ref(false)
const error = ref(false)

const form = reactive({
  title_ja: '',
  title_en: '',
  body_ja: '',
  body_en: '',
  target_role: 'all',
  is_important: false,
})

async function handleSubmit() {
  loading.value = true
  error.value = false
  try {
    await createNotice(form)
    success.value = true
    setTimeout(() => router.push({ name: 'admin-notices' }), 1000)
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}
</script>
