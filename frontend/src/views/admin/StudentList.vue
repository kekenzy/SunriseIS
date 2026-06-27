<template>
  <div class="p-6 max-w-5xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">園児・保護者管理</h1>

    <div class="flex gap-3 mb-6">
      <input v-model="query" @input="search" placeholder="名前・クラスで検索..."
        class="input-field max-w-xs" />
    </div>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <div v-else class="card overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-sand/40 text-left border-b border-navy-800">
            <th class="pb-3">園児名</th>
            <th class="pb-3">英語名</th>
            <th class="pb-3">クラス</th>
            <th class="pb-3">入園日</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="child in students" :key="child.id" class="border-b border-navy-800 last:border-0 hover:bg-navy-800/50">
            <td class="py-3 text-sand font-medium">{{ child.name_ja }}</td>
            <td class="py-3 text-sand/60">{{ child.name_en }}</td>
            <td class="py-3 text-sand/70">{{ child.class_name }}</td>
            <td class="py-3 text-sand/50">{{ child.enrolled_at }}</td>
          </tr>
          <tr v-if="!students.length">
            <td colspan="4" class="py-8 text-center text-sand/40">該当する園児が見つかりません</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminStudents } from '@/api/admin'

const students = ref([])
const loading = ref(true)
const query = ref('')
let timer = null

async function load(q = '') {
  const { data } = await getAdminStudents(q)
  students.value = data
}

function search() {
  clearTimeout(timer)
  timer = setTimeout(() => load(query.value), 300)
}

onMounted(async () => {
  try { await load() } finally { loading.value = false }
})
</script>
