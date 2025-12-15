<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useCreateRental } from '~/composables/useCreateRental'
import { useCreatePurchase } from '~/composables/useCreatePurchase'

interface Props {
  availability: 'rent' | 'purchase' | 'both'
  dailyRentPrice?: number
  securityDeposit?: number
  purchasePrice?: number
  rentalDuration?: number
  bookId: string
  rentalExists: boolean
  purchaseExists: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  rent: []
  purchase: []
}>()

const { checkRentalExists } = useCreateRental()

const { checkPurchaseExists } = useCreatePurchase()

onMounted(async () => {
  if (props.bookId) {
    await checkRentalExists(props.bookId)
    await checkPurchaseExists(props.bookId)
  }
})

const openRentBookModal = () => {
  emit('rent')
};

const openPurchaseBookModal = () => {
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
          <div class="flex justify-between items-center">
            <span class="flex items-center gap-1 text-base">
              <UIcon name="i-heroicons-clock" class="text-base w-5 h-5" />
              Duration
            </span>
            <span class="font-bold text-accent">
              {{ rentalDuration }} {{ rentalDuration === 1 ? 'day' : 'days' }}
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
        @click="openRentBookModal"
        :disabled="props.rentalExists"
        class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2 cursor-pointer disabled:bg-blue-400 disabled:dark:bg-blue-600 disabled:text-white disabled:cursor-not-allowed"
      >
        <UIcon name="i-heroicons-book-open" class="text-xl" />
        <span v-if="props.rentalExists">Request Already Sent</span>
        <span v-else>Rent This Book</span>
      </button>
      
      <button 
        v-if="availability === 'purchase' || availability === 'both'"
        @click="openPurchaseBookModal"
        :disabled="props.purchaseExists"
        class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2 cursor-pointer disabled:bg-blue-400 disabled:dark:bg-blue-600 disabled:text-white disabled:cursor-not-allowed"
      >
        <UIcon name="i-heroicons-shopping-cart" class="text-xl" />
        <span v-if="props.purchaseExists">Request Already Sent</span>
        <span v-else>Buy This Book</span>
      </button>
    </div>
  </UCard>
</template>