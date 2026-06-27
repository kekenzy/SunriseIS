<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-sand mb-6">{{ $t('nav.events') }}</h1>

    <div v-if="loading" class="text-sand/50 text-center py-20">{{ $t('common.loading') }}</div>

    <ul v-else class="space-y-4">
      <li v-for="ev in events" :key="ev.id" class="card">
        <div class="flex justify-between items-start mb-3">
          <div>
            <h2 class="text-sand font-semibold">{{ ev.title_ja }}</h2>
            <p class="text-sand/50 text-sm mt-1">{{ ev.event_date }} {{ ev.time_range }}{{ ev.place ? ' · ' + ev.place : '' }}</p>
          </div>
          <span v-if="ev.rsvp_status" :class="['text-xs px-2 py-1 rounded font-semibold',
            ev.rsvp_status === 'attending' ? 'bg-teal-600/20 text-teal-400' : 'bg-red-500/20 text-red-400']">
            {{ ev.rsvp_status === 'attending' ? '参加' : '不参加' }}
          </span>
          <span v-else class="text-xs text-sand/40">回答待ち</span>
        </div>

        <div class="flex gap-2">
          <button @click="rsvp(ev, 'attending')" :disabled="ev.rsvp_status === 'attending'"
            :class="['text-sm py-1.5 px-4 rounded-lg transition-colors', ev.rsvp_status === 'attending' ? 'bg-teal-600 text-white cursor-default' : 'btn-ghost border border-teal-600/40']">
            参加
          </button>
          <button @click="rsvp(ev, 'not_attending')" :disabled="ev.rsvp_status === 'not_attending'"
            :class="['text-sm py-1.5 px-4 rounded-lg transition-colors', ev.rsvp_status === 'not_attending' ? 'bg-red-500/30 text-red-400 cursor-default' : 'btn-ghost border border-red-500/20']">
            不参加
          </button>
        </div>
      </li>

      <li v-if="!events.length" class="text-sand/40 text-center py-12">今後のイベントはありません</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEvents, postRsvp } from '@/api/parent'

const events = ref([])
const loading = ref(true)

async function load() {
  const { data } = await getEvents()
  events.value = data
}

async function rsvp(ev, status) {
  await postRsvp(ev.id, status)
  ev.rsvp_status = status
}

onMounted(async () => {
  try { await load() } finally { loading.value = false }
})
</script>
