<script setup lang="ts">
import type { Rental } from '~/composables/useUserRentals';
import type { Lending } from '~/composables/useUserLendings';

interface Props {
  status: string;
  from: string;
  actualDeposit: number;
  item: Rental | Lending;
}

const props = defineProps<Props>();
const emit = defineEmits(['show-rating']);

const userName = computed(() => {
  return props.from === 'rental' 
    ? (props.item as Rental).from 
    : (props.item as Lending).to;
});

const userRole = computed(() => {
  return props.from === 'rental' ? 'lender' : 'renter';
});

const handleRateUser = () => {
  emit('show-rating');
};
</script>

<template>
  <div class="space-y-6">
    <!-- Deposit Return Card -->
    <div class="bg-green-50 border border-green-200 rounded-lg p-5">
      <div class="flex items-start gap-3">
        <Icon name="lucide:check-circle" class="w-6 h-6 text-green-600 mt-0.5 flex-shrink-0" />
        <div class="flex-1">
          <p class="text-green-900 font-medium text-lg mb-1">
            Security deposit {{ from === 'rental' ? 'has returned to you' : 'has returned to the renter' }}
          </p>
          <div class="flex items-center gap-2 mt-2">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-green-600" />
            <span class="text-green-800 font-bold text-xl">{{ props.actualDeposit }} Readits</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Completed Message -->
    <div class="bg-surface rounded-lg border border-base p-6 py-8">
      <div class="text-center">
        <Icon name="lucide:check-circle" class="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 class="text-2xl font-bold mb-2">Rental Completed!</h2>
        <p class="text-muted mb-6">We're glad to have been part of your reading journey. Feel free to explore more titles anytime!</p>
        
        <!-- Rate User Button -->
        <button 
          @click="handleRateUser"
          class="bg-accent hover:bg-accent/90 text-white px-6 py-3 rounded-lg font-medium transition-colors inline-flex items-center gap-2 cursor-pointer"
        >
          <Icon name="lucide:star" class="w-5 h-5" />
          Rate {{ from === 'rental' ? 'Lender' : 'Renter' }}
        </button>
      </div>
    </div>
  </div>
</template>