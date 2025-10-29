<script setup lang="ts">
interface Props {
  availability: 'rent' | 'purchase' | 'both'
  dailyRentPrice?: number
  securityDeposit?: number
  purchasePrice?: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  rent: []
  purchase: []
}>()

const handleRent = () => {
  emit('rent')
}

const handlePurchase = () => {
  emit('purchase')
}
</script>

<template>
  <UCard class="bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800">
    <h2 class="font-semibold text-lg mb-4 flex items-center gap-2 text-base">
      <UIcon name="fluent:book-coins-20-regular" class="text-xl w-7 h-7" />
      Pricing Options
    </h2>

    <div 
      class="grid gap-4"
      :class="availability === 'both' ? 'md:grid-cols-2' : 'grid-cols-1'"
    >
      <!-- Rental Option -->
      <div 
        v-if="availability === 'rent' || availability === 'both'"
        class="bg-blue-100 dark:bg-blue-900/30 rounded-lg p-4 border-2 border-blue-200 dark:border-blue-700"
      >
        <h3 class="text-blue-700 dark:text-blue-400 font-semibold mb-3 flex items-center gap-2">
          <UIcon name="i-heroicons-book-open" class="text-xl" />
          Rental Option
        </h3>
        
        <div class="space-y-2 text-sm mb-3">
          <div class="flex justify-between items-center">
            <span class="flex items-center gap-1 text-base">
              <UIcon name="i-heroicons-calendar" class="text-base w-5 h-5" />
              Daily Rate
            </span>
            <span class="flex font-bold text-accent items-center">
                <UIcon name="fluent:book-coins-20-regular" class="w-5 h-5"/>
                {{ dailyRentPrice }}
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="flex items-center gap-1 text-base">
              <UIcon name="i-heroicons-shield-check" class="text-base w-5 h-5" />
              Deposit
            </span>
            <span class="flex items-center font-bold text-accent">
                <UIcon name="fluent:book-coins-20-regular" class="w-5 h-5"/>
                {{ securityDeposit }}
            </span>
          </div>
        </div>
        
        <div class="text-xs text-muted bg-surface/50 rounded p-2 flex items-start gap-2">
          <UIcon name="i-heroicons-shield-check" class="text-sm flex-shrink-0 mt-0.5 w-4 h-4" />
          <span>Deposit refunded upon safe return</span>
        </div>
      </div>

      <!-- Purchase Option -->
      <div 
        v-if="availability === 'purchase' || availability === 'both'"
        class="bg-green-100 dark:bg-green-900/30 rounded-lg p-4 border-2 border-green-200 dark:border-green-700"
      >
        <h3 class="text-green-700 dark:text-green-400 font-semibold mb-3 flex items-center gap-2">
          <UIcon name="i-heroicons-shopping-cart" class="text-xl" />
          Purchase Option
        </h3>
        
        <div class="space-y-2 text-sm mb-3">
          <div class="flex justify-between items-center">
            <span class="flex items-center gap-1 text-base">
              <UIcon name="i-heroicons-currency-dollar" class="text-base w-5 h-5" />
              One-time Price
            </span>
            <span class="flex items-center font-bold text-accent">
                <UIcon name="fluent:book-coins-20-regular" class="w-5 h-5"/>
                {{ purchasePrice }}
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-base">Ownership</span>
            <span class="font-bold text-accent">Forever</span>
          </div>
        </div>
        
        <div class="text-xs text-muted bg-surface/50 rounded p-2 flex items-start gap-2">
          <UIcon name="i-heroicons-shopping-cart" class="text-sm flex-shrink-0 mt-0.5" />
          <span>Own the book permanently - no returns needed</span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div 
      class="grid gap-3 mt-6"
      :class="availability === 'both' ? 'md:grid-cols-2' : 'grid-cols-1'"
    >
      <button 
        v-if="availability === 'rent' || availability === 'both'"
        @click="handleRent"
        class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2 cursor-pointer"
      >
        <UIcon name="i-heroicons-book-open" class="text-xl" />
        Rent This Book
      </button>
      
      <button 
        v-if="availability === 'purchase' || availability === 'both'"
        @click="handlePurchase"
        class="bg-green-700 hover:bg-green-800 dark:bg-green-500 dark:hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2 cursor-pointer"
      >
        <UIcon name="i-heroicons-shopping-cart" class="text-xl" />
        Buy This Book
      </button>
    </div>
  </UCard>
</template>