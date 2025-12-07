<script setup lang="ts">
import type { Purchase } from '~/composables/useUserPurchases';
import type { Sale } from '~/composables/useUserSales';

interface Props {
  item: Purchase | Sale;
  from: string;
  isCompleted?: boolean;
}

const props = defineProps<Props>();

const getStatusBadge = (status: string) => {
  const statusConfig: Record<string, { label: string; color: string }> = {
    pending: { label: 'Pending Approval', color: 'bg-yellow-500' },
    approved: { label: 'Confirmed', color: 'bg-blue-500' },
    awaiting_pickup_confirmation: { label: 'Pickup Arranged', color: 'bg-orange-500' },
    completed: { label: 'Completed', color: 'bg-green-500' },
    rate_user: { label: 'Rate User', color: 'bg-amber-500' },
  };

  return statusConfig[status] || { label: status, color: 'bg-gray-500' };
};

const userName = computed(() => {
  return props.from === 'purchase' ? (props.item as Purchase).from : (props.item as Sale).to;
});

console.log(props.item);
</script>

<template>
  <div class="bg-surface rounded-lg border border-base p-6">
    <div class="flex gap-6">
      <img :src="item.image" :alt="item.title" class="w-32 h-48 object-cover rounded-lg" />
      <div class="flex-1">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bold mb-1">{{ item.title }}</h2>
            <p class="text-muted">by {{ item.author }}</p>
          </div>
          <span
            :class="[
              getStatusBadge(item.purchase_status).color,
              'text-white px-4 py-2 rounded-full text-sm font-medium',
            ]"
          >
            {{ getStatusBadge(item.purchase_status).label }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-4 mt-6">
          <div>
            <p v-if="props.isCompleted" class="text-sm text-muted">
              {{ from === 'purchase' ? 'Bought from' : 'Sold to' }}
            </p>

            <p v-else class="text-sm text-muted">
              {{ from === 'purchase' ? 'Buying from' : 'Selling to' }}
            </p>

            <NuxtLink
              v-if="from === 'purchase'"
              :to="`/users/${item.user_id}`"
              class="font-medium text-lg"
              >{{ userName }}
            </NuxtLink>

            <NuxtLink v-else :to="`/users/${item.original_owner_id}`" class="font-medium text-lg">
              {{ userName }}
            </NuxtLink>
          </div>
          <div>
            <p class="text-sm text-muted">Transaction Type</p>
            <p class="font-medium text-lg">Purchase</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
