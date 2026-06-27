<template>
  <div class="p-6 max-w-5xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">請求管理</h1>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <div v-else class="card overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-sand/40 text-left border-b border-navy-800">
            <th class="pb-3">対象月</th>
            <th class="pb-3">内容</th>
            <th class="pb-3 text-right">金額</th>
            <th class="pb-3 text-right">状況</th>
            <th class="pb-3">期日</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bill in bills" :key="bill.id" class="border-b border-navy-800 last:border-0">
            <td class="py-3 text-sand/70">{{ bill.month }}</td>
            <td class="py-3 text-sand">{{ bill.description_ja }}</td>
            <td class="py-3 text-right text-sand font-medium">¥{{ bill.amount.toLocaleString() }}</td>
            <td class="py-3 text-right">
              <span :class="bill.status === 'paid' ? 'text-teal-400' : 'text-red-400'" class="text-xs font-semibold">
                {{ bill.status === 'paid' ? '支払済' : '未払い' }}
              </span>
            </td>
            <td class="py-3 text-sand/50">{{ bill.due_date ?? '-' }}</td>
          </tr>
          <tr v-if="!bills.length">
            <td colspan="5" class="py-8 text-center text-sand/40">請求データがありません</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminBills } from '@/api/admin'

const bills = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await getAdminBills()
    bills.value = data
  } finally {
    loading.value = false
  }
})
</script>
