<script setup lang="ts">
import type { Purchase } from '~/composables/useUserPurchases';
import type { Sale } from '~/composables/useUserSales';

interface Props {
  item: Purchase | Sale;
  from: string;
}

const props = defineProps<Props>();

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

const formatDateTime = (dateString: string) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC',
    timeZoneName: 'short'
  });
}
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- Dates Card -->
    <div class="bg-surface rounded-lg border border-base p-6">
      <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
        <Icon name="lucide:calendar" class="w-5 h-5" />
        Important Dates
      </h3>
      <div class="space-y-4">
        <div v-if="item.reserved_at">
          <p class="text-sm text-muted">Reserved At</p>
          <p class="font-medium">{{ formatDateTime(item.reserved_at) }}</p>
        </div>

        <div v-if="item.reservation_expires_at && item.purchase_status === 'pending'">
          <p class="text-sm text-muted">Reservation Expires</p>
          <p class="font-medium text-red-600">{{ formatDateTime(item.reservation_expires_at) }}</p>
        </div>

        <div v-if="item.meetup_date">
          <p class="text-sm text-muted">Meetup Date</p>
          <p class="font-medium">{{ formatDate(item.meetup_date) }}</p>
        </div>
      </div>
    </div>

    <!-- Meetup Information Card -->
    <div class="bg-surface rounded-lg border border-base p-6">
      <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
        <Icon name="lucide:map-pin" class="w-5 h-5" />
        Meetup Information
      </h3>
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div v-if="item.meetup_time">
            <p class="text-sm text-muted">Meetup Time</p>
            <p class="font-medium">{{ item.meetup_time }}</p>
          </div>

          <div v-if="item.meetup_time_window">
            <p class="text-sm text-muted">Time Window</p>
            <p class="font-medium">{{ item.meetup_time_window }}</p>
          </div>
        </div>

        <div>
          <p class="text-sm text-muted">Meetup Location</p>
          <p class="font-medium">{{ item.meetup_location || 'Not set' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>