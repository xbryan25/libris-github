<script setup lang="ts">
import type { Rental } from '~/composables/useUserRentals';
import type { Lending } from '~/composables/useUserLendings';

interface Props {
  item: Rental | Lending;
  from: string;
}

const props = defineProps<Props>();

const getStatusBadge = (status: string) => {
  const statusConfig: Record<string, { label: string; color: string }> = {
    pending: { label: 'Pending Approval', color: 'bg-yellow-500' },
    approved: { label: 'Confirmed', color: 'bg-blue-500' },
    awaiting_pickup_confirmation: { label: 'Pickup Arranged', color: 'bg-orange-500' },
    ongoing: { label: 'Book Received', color: 'bg-purple-500' },
    awaiting_return_confirmation: { label: 'Return Initiated', color: 'bg-indigo-500' },
    completed: { label: 'Completed', color: 'bg-green-500' },
    rate_user: { label: 'Rate User', color: 'bg-amber-500' }
  }
  
  return statusConfig[status] || { label: status, color: 'bg-gray-500' }
}

const userName = computed(() => {
  return props.from === 'rental' 
    ? (props.item as Rental).from 
    : (props.item as Lending).to;
});
</script>

<template>
  <div class="bg-surface rounded-lg border border-base p-6">
    <div class="flex gap-6">
      <img 
        :src="item.image" 
        :alt="item.title"
        class="w-32 h-48 object-cover rounded-lg"
      />
      <div class="flex-1">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bold mb-1">{{ item.title }}</h2>
            <p class="text-muted">by {{ item.author }}</p>
          </div>
          <span 
            :class="[getStatusBadge(item.rent_status).color, 'text-white px-4 py-2 rounded-full text-sm font-medium']"
          >
            {{ getStatusBadge(item.rent_status).label }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-4 mt-6">
          <div>
            <p class="text-sm text-muted">{{ from === 'rental' ? 'Renting from' : 'Lending to' }}</p>
            <p class="font-medium text-lg">{{ userName }}</p>
          </div>
          <div>
            <p class="text-sm text-muted">Duration</p>
            <p class="font-medium text-lg">{{ item.rental_duration_days }} days</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>