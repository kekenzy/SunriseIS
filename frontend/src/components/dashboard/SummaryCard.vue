<template>
  <div
    :class="['card flex flex-col gap-1', clickable ? 'cursor-pointer hover:bg-navy-800 transition-colors' : '']"
    @click="clickable ? $emit('click') : null"
  >
    <span class="text-2xl">{{ icon }}</span>
    <p class="text-sand/50 text-xs">{{ label }}</p>
    <p class="text-sand font-bold text-lg leading-tight">{{ value }}</p>
    <p v-if="sub" class="text-sand/40 text-xs">{{ sub }}</p>
  </div>
</template>

<script setup>
defineProps({
  icon: String,
  label: String,
  value: String,
  sub: String,
  clickable: Boolean,
})
defineEmits(['click'])
</script>
