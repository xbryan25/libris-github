<script setup lang="ts">
import type { Rental } from '~/composables/useUserRentals';
import type { StepperItem } from '@nuxt/ui';

interface Props {
  rental: Rental;
}

defineProps<Props>();

const getStatusBadge = (status: string) => {
  const statusConfig: Record<string, { label: string; color: string }> = {
    pending: { label: 'Pending Approval', color: 'bg-yellow-500' },
    approved: { label: 'Confirmed', color: 'bg-blue-500' },
    awaiting_pickup_confirmation: { label: 'Pickup Arranged', color: 'bg-orange-500' },
    ongoing: { label: 'Book Received', color: 'bg-purple-500' },
    awaiting_return_confirmation: { label: 'Return Initiated', color: 'bg-indigo-500' },
    completed: { label: 'Return Complete', color: 'bg-green-500' },
    rate_user: { label: 'Rate User', color: 'bg-amber-500' },
  };

  return statusConfig[status] || { label: status, color: 'bg-gray-500' };
};

const getStepperItems = (status: string): StepperItem[] => {
  return [
    {
      title: 'Requested',
      description: 'Rental request sent',
      icon: 'i-lucide-send',
    },
    {
      title: 'Confirmed',
      description: 'Owner approved request',
      icon: 'i-lucide-check-circle',
    },
    {
      title: 'Pickup',
      description: 'Ready for pickup',
      icon: 'i-lucide-package',
    },
    {
      title: 'Renting',
      description: 'Currently renting',
      icon: 'i-lucide-book-open',
    },
    {
      title: 'Return',
      description: 'Ready for return',
      icon: 'i-lucide-package-check',
    },
    {
      title: 'Completed',
      description: 'Rental finished',
      icon: 'i-lucide-circle-check',
    },
    {
      title: 'Rate',
      description: 'Rate the experience',
      icon: 'i-lucide-star',
    },
  ];
};

const getCurrentStep = (status: string) => {
  const statusMap: Record<string, number> = {
    pending: 0,
    approved: 1,
    awaiting_pickup_confirmation: 2,
    ongoing: 3,
    awaiting_return_confirmation: 4,
    completed: 5,
  };

  return statusMap[status] ?? 0;
};
</script>

<template>
  <NuxtLink
    :to="{
      path: `/rentals/${rental.rental_id}`,
      query: { from: 'rental' },
    }"
    class="block"
  >
    <div class="bg-surface rounded-lg border border-base p-6 hover:shadow-md transition-shadow">
      <!-- Header -->
      <div class="flex justify-between items-start mb-4">
        <div class="flex-1">
          <h3 class="text-xl font-bold text-foreground mb-2">{{ rental.title }}</h3>
          <div class="flex items-center gap-4 text-sm text-muted">
            <div class="flex items-center gap-1">
              <Icon name="lucide:user" class="w-4 h-4" />
              <span>Renting from {{ rental.from }}</span>
            </div>
            <div class="flex items-center gap-1">
              <Icon name="lucide:calendar" class="w-4 h-4" />
              <span>{{ rental.rental_duration_days }} Days</span>
            </div>
          </div>
        </div>

        <!-- Status Badge and Readits -->
        <div class="flex items-center gap-3">
          <span
            :class="[
              getStatusBadge(rental.rent_status).color,
              'text-white px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap',
            ]"
          >
            {{ getStatusBadge(rental.rent_status).label }}
          </span>
          <div class="flex items-center gap-1">
            <span class="text-accent text-xl font-bold">-</span>
            <Icon name="fluent:book-coins-20-regular" class="w-6 h-6 text-accent" />
            <span class="text-accent text-xl font-bold">{{ rental.cost }}</span>
          </div>
        </div>
      </div>

      <!-- Progress Steps using UStepper -->
      <div class="mt-6">
        <UStepper
          disabled
          :items="getStepperItems(rental.rent_status)"
          :model-value="getCurrentStep(rental.rent_status)"
        />
      </div>
    </div>
  </NuxtLink>
</template>
