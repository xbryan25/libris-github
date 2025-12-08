<script setup lang="ts">
import type { Rental } from '~/composables/useUserRentals';

interface Props {
  rental: Rental;
}

const props = defineProps<Props>();

const convertDateFormat = (dateString: string) => {
  try {
    const [yearStr, monthStr, dayStr] = dateString.split('-').map(Number);

    const month: number = Number(monthStr);
    const day: number = Number(dayStr);
    const year: number = Number(yearStr);

    const date = new Date(year, month - 1, day); // JS months are 0-based

    const formatted = date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });

    return formatted;
  } catch {
    return 'null';
  }
};
</script>

<template>
  <NuxtLink
    :to="{
      path: `/rentals/history/${rental.rental_id}`,
      query: { from: 'rental' },
    }"
    class="block"
  >
    <div
      class="bg-surface rounded-lg border border-base px-6 py-5 hover:shadow-md transition-shadow"
    >
      <!-- Header -->
      <div class="flex justify-between items-start">
        <div class="flex-1">
          <h3 class="text-xl font-bold text-foreground mb-2">{{ rental.title }}</h3>
          <div class="flex items-center gap-4 text-sm text-muted">
            <div class="flex items-center gap-1">
              <Icon name="lucide:user" class="w-4 h-4" />
              <span>Rented from {{ rental.from }}</span>
            </div>
            <div class="flex items-center gap-1">
              <Icon name="lucide:calendar" class="w-4 h-4" />
              <span
                >{{ convertDateFormat(rental.rent_start_date) }} -
                {{ convertDateFormat(rental.rent_end_date) }}</span
              >
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1">
            <span class="text-accent text-xl font-bold">-</span>
            <Icon name="fluent:book-coins-20-regular" class="w-6 h-6 text-accent" />
            <span class="text-accent text-xl font-bold">{{ rental.cost }}</span>
          </div>
        </div>
      </div>
    </div>
  </NuxtLink>
</template>
