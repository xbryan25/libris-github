<script setup lang="ts">
import LendCard from '~/components/LendCard.vue';
import { useUserRentals } from '~/composables/useUserRentals';

interface Props {
  activeTab: 'lending' | 'renting';
}

defineProps<Props>();

const {
  rentals,
  loading: rentalsLoading,
  error: rentalsError,
  fetchUserRentals,
} = useUserRentals();
const {
  lendings,
  loading: lendingsLoading,
  error: lendingsError,
  fetchUserLendings,
} = useUserLendings();

onMounted(() => {
  fetchUserRentals();
  fetchUserLendings();
});
</script>

<template>
  <div class="w-full bg-background">
    <div v-if="activeTab === 'lending'">
      <!-- Lending content -->
      <div v-if="lendingsLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your Lendings...</p>
          </div>
        </div>
      </div>

      <div v-else-if="lendingsError" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:alert-circle" class="w-16 h-16 text-red-500 mx-auto" />
            <p class="text-red-500 mt-4 text-lg">{{ lendingsError }}</p>
          </div>
        </div>
      </div>

      <div
        v-else-if="lendings.length === 0"
        class="bg-surface rounded-lg p-6 w-full border border-base"
      >
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="bytesize:book" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">No active lendings</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <LendCard v-for="lending in lendings" :key="lending.rental_id" :lending="lending" />
      </div>
    </div>

    <div v-else>
      <!-- Renting content -->
      <div v-if="rentalsLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your rentals...</p>
          </div>
        </div>
      </div>

      <div v-else-if="rentalsError" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:alert-circle" class="w-16 h-16 text-red-500 mx-auto" />
            <p class="text-red-500 mt-4 text-lg">{{ rentalsError }}</p>
          </div>
        </div>
      </div>

      <div
        v-else-if="rentals.length === 0"
        class="bg-surface rounded-lg p-6 w-full border border-base"
      >
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="bytesize:book" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">No active rentals</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <RentalCard v-for="rental in rentals" :key="rental.rental_id" :rental="rental" />
      </div>
    </div>
  </div>
</template>
