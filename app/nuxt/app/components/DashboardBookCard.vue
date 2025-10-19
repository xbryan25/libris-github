<script setup>
import { computed } from 'vue'

const props = defineProps({
  book: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ['renting', 'bought', 'rented-by-others', 'bought-by-others'].includes(value)
  }
})

const badgeText = computed(() => {
  switch (props.type) {
    case 'renting':
      return `Renting from ${props.book.from}`
    case 'bought':
      return `Bought from ${props.book.from}`
    case 'rented-by-others':
      return `Rented by ${props.book.by}`
    case 'bought-by-others':
      return `Bought by ${props.book.by}`
    default:
      return ''
  }
})

const badgeClasses = computed(() => {
  const baseClasses = 'inline-block text-xs font-medium px-2.5 py-1 rounded mb-2.5 text-white'
  
  const colorClass = {
    'renting': 'bg-blue-600',
    'bought': 'bg-green-600',
    'rented-by-others': 'bg-purple-600',
    'bought-by-others': 'bg-orange-600'
  }[props.type]
  
  return `${baseClasses} ${colorClass}`
})

const dateText = computed(() => {
  if (props.type === 'renting' && props.book.returnDate) {
    return `Return on ${props.book.returnDate}`
  }
  if (props.type === 'rented-by-others' && props.book.returnDate) {
    return `Will be returned on ${props.book.returnDate}`
  }
  return null
})

const costLabel = computed(() => {
  switch (props.type) {
    case 'renting':
    case 'rented-by-others':
      return 'Total rent cost'
    case 'bought':
    case 'bought-by-others':
      return 'Total cost'
    default:
      return 'Total cost'
  }
})
</script>

<template>
  <div class="flex-shrink-0 border border-base rounded-lg overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-lg bg-surface-hover cursor-pointer">
    <div class="w-full h-72 overflow-hidden">
      <img :src="book.image" :alt="book.title" class="w-full h-full object-cover" />
    </div>
    
    <div class="p-4 text-base">
      <h3 class="font-semibold mb-1">
        {{ book.title }}
      </h3>
      <p class="text-sm text-muted mb-2.5">
        by {{ book.author }}
      </p>
      
      <!-- Badge -->
      <span :class="badgeClasses">
        {{ badgeText }}
      </span>
      
      <!-- Date info -->
      <div v-if="dateText" class="flex items-center gap-1 text-xs mb-1">
        <Icon name="mingcute:time-line" class="w-3 h-3" />
        <span>{{ dateText }}</span>
      </div>
      
      <!-- Cost info -->
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-1 text-xs">
          <Icon name="material-symbols:shopping-cart-outline-rounded" class="w-3 h-3" />
          <span>{{ costLabel }}</span>
        </div>
        <span class="text-sm font-bold text-accent">{{ book.cost }}</span>
      </div>
    </div>
  </div>
</template>
