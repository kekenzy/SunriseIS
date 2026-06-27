<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">{{ $t('nav.payment') }}</h1>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <template v-else>
      <!-- 未払い合計 -->
      <div v-if="unpaidTotal > 0" class="card bg-teal-600/10 border border-teal-600/30 mb-6">
        <p class="text-sand/60 text-sm mb-1">未払い合計</p>
        <p class="text-3xl font-bold text-teal-400">¥{{ unpaidTotal.toLocaleString() }}</p>
      </div>

      <!-- 請求一覧 -->
      <div class="card">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-sand/40 text-left border-b border-navy-800">
              <th class="pb-2">対象月</th>
              <th class="pb-2">内容</th>
              <th class="pb-2 text-right">金額</th>
              <th class="pb-2 text-right">状況</th>
              <th class="pb-2"></th>
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
              <td class="py-3 text-right">
                <button v-if="bill.status === 'unpaid'"
                  @click="handlePay(bill)"
                  :disabled="paying === bill.id"
                  class="btn-primary text-xs py-1 px-3">
                  {{ paying === bill.id ? '処理中…' : '支払う' }}
                </button>
                <span v-else-if="bill.has_receipt" class="text-teal-600/60 text-xs">領収書 ✓</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- お支払い方法 -->
      <div class="card mt-4">
        <p class="text-sand/60 text-sm mb-2">お支払い方法</p>
        <p class="text-sand text-sm">💳 クレジットカード •••• 4218</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getBills, payBill } from '@/api/parent'

const bills = ref([])
const loading = ref(true)
const paying = ref(null)

const unpaidTotal = computed(() =>
  bills.value.filter(b => b.status === 'unpaid').reduce((sum, b) => sum + b.amount, 0)
)

async function load() {
  const { data } = await getBills()
  bills.value = data
}

async function handlePay(bill) {
  paying.value = bill.id
  try {
    const { data } = await payBill(bill.id)
    const idx = bills.value.findIndex(b => b.id === bill.id)
    if (idx !== -1) bills.value[idx] = data
  } finally {
    paying.value = null
  }
}

onMounted(async () => {
  try { await load() } finally { loading.value = false }
})
</script>
