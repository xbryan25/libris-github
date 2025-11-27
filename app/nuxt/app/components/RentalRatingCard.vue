<script setup lang="ts">
import type { Rental } from '~/composables/useUserRentals';
import type { Lending } from '~/composables/useUserLendings';

interface Props {
  status: string;
  from: string;
  deposit: number;
  item: Rental | Lending;
}

const props = defineProps<Props>();

const userName = computed(() => {
  return props.from === 'rental' 
    ? (props.item as Rental).from 
    : (props.item as Lending).to;
});

const userRole = computed(() => {
  return props.from === 'rental' ? 'lender' : 'renter';
});
</script>

<template>
  <div class="space-y-6">
    <!-- Deposit Return Card -->
    <div class="bg-green-50 border border-green-200 rounded-lg p-5">
      <div class="flex items-start gap-3">
        <Icon name="lucide:check-circle" class="w-6 h-6 text-green-600 mt-0.5 flex-shrink-0" />
        <div class="flex-1">
          <p class="text-green-900 font-medium text-lg mb-1">
            Security deposit {{ from === 'rental' ? 'has been returned' : 'returned' }}
          </p>
          <div class="flex items-center gap-2 mt-2">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-green-600" />
            <span class="text-green-800 font-bold text-xl">{{ props.deposit }} Readits</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Rating Card - Only show if status is rate_user -->
    <div v-if="status === 'rate_user'" class="bg-surface rounded-lg border border-base p-6">
      <h2 class="text-2xl font-bold text-center mb-2">
        Rate {{ userName }} as a {{ userRole }}
      </h2>
      <p class="text-center text-muted mb-6">How would you rate this user?</p>
      
      <!-- rating stuff herer-->

    </div>

    <!-- Completed Message - Show if status is completed -->
    <div v-if="status === 'completed'" class="bg-surface rounded-lg border border-base p-6">
      <div class="text-center">
        <Icon name="lucide:check-circle" class="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 class="text-2xl font-bold mb-2">Rental Completed!</h2>
        <p class="text-muted">Thank you for using our service. Your rating has been submitted.</p>
      </div>
    </div>
  </div>
</template>