<script setup lang="ts">
import type { Purchase } from '~/composables/useUserPurchases';
import type { Sale } from '~/composables/useUserSales';

interface Props {
  status: string;
  from: string;
  item: Purchase | Sale;
}

const props = defineProps<Props>();
const emit = defineEmits(['show-rating']);

const userName = computed(() => {
  return props.from === 'purchase' 
    ? (props.item as Purchase).from 
    : (props.item as Sale).to;
});

const handleRateUser = () => {
  emit('show-rating');
};
</script>

<template>
  <div class="space-y-6">
    <!-- Completed Message -->
    <div class="bg-surface rounded-lg border border-base p-6 py-8">
      <div class="text-center">
        <Icon name="lucide:check-circle" class="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 class="text-2xl font-bold mb-2">
          {{ from === 'purchase' ? 'Purchase Completed!' : 'Sale Completed!' }}
        </h2>
        <p class="text-muted mb-6">
          {{ from === 'purchase' 
            ? 'Thank you for your purchase! We hope you enjoy your new book.' 
            : 'Congratulations on your sale! The transaction has been completed successfully.' 
          }}
        </p>
        
        <!-- Rate User Button -->
        <button 
          @click="handleRateUser"
          class="bg-accent hover:bg-accent/90 text-white px-6 py-3 rounded-lg font-medium transition-colors inline-flex items-center gap-2 cursor-pointer"
        >
          <Icon name="lucide:star" class="w-5 h-5" />
          Rate {{ from === 'purchase' ? 'Seller' : 'Buyer' }}
        </button>
      </div>
    </div>
  </div>
</template>