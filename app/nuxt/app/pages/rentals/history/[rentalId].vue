<script setup lang="ts">
import auth from '~/middleware/auth';
import { useUserRentals, type Rental } from '~/composables/useUserRentals';
import { useUserLendings, type Lending } from '~/composables/useUserLendings';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const rentalId = route.params.rentalId as string;
const from = route.query.from as string;

const { rentals, fetchUserCompletedRental } = useUserRentals();
const { lendings, fetchUserCompletedLending } = useUserLendings();

const currentItem = ref<Rental | Lending | null>(null);
const loading = ref(true);

const fetchRentalData = async () => {
  loading.value = true;

  console.log('reach here');

  try {
    if (from === 'rental') {
      await fetchUserCompletedRental(rentalId);
      currentItem.value = rentals.value[0] ?? null;
    } else if (from === 'lending') {
      await fetchUserCompletedLending(rentalId);
      currentItem.value = lendings.value[0] ?? null;
    }
  } catch (error) {
    console.error('Error fetching rental data:', error);
  } finally {
    loading.value = false;
  }

  console.log(currentItem.value);
};

onMounted(() => {
  fetchRentalData();
});
</script>

<template>
  <div class="min-h-screen w-full pt-4 pb-6 px-4 md:px-8 lg:px-15">
    <!-- Header -->
    <div class="mb-6">
      <NuxtLink
        :to="`/rentals/history?activeTab=${from === 'rental' ? 'renting' : 'lending'}`"
        class="flex items-center gap-2 text-base pt-4 pb-4 hover:text-foreground mb-4 cursor-pointer"
      >
        <Icon name="lucide:arrow-left" class="w-5 h-5" />
        <span>Back to {{ from === 'rental' ? 'Rentals' : 'Lendings' }} History</span>
      </NuxtLink>

      <h1 class="font-bold text-3xl flex items-center gap-2 mb-1">
        <Icon
          :name="from === 'rental' ? 'lucide:trending-down' : 'lucide:trending-up'"
          class="w-8 h-8 text-orange-500"
        />
        {{ from === 'rental' ? 'Rental Details' : 'Lending Details' }}
      </h1>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface rounded-lg border border-base p-12">
      <div class="flex justify-center items-center">
        <div class="text-center">
          <Icon name="lucide:loader-2" class="w-12 h-12 text-muted mx-auto animate-spin" />
          <p class="text-muted mt-4 text-lg">Loading details...</p>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else-if="!currentItem" class="bg-surface rounded-lg border border-base p-12">
      <div class="flex justify-center items-center">
        <div class="text-center">
          <Icon name="lucide:alert-circle" class="w-16 h-16 text-red-500 mx-auto" />
          <p class="text-red-500 mt-4 text-lg">Rental not found</p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Book Info Card (Hide when completed) -->
      <RentalBookInfoCard :item="currentItem" :from="from" :is-completed="true" />

      <!-- Dates & Meetup Grid -->
      <RentalDetailsGrid :item="currentItem" :from="from" />

      <!-- Cost Card -->
      <RentalCostCard
        :cost="currentItem.cost"
        :all-fees-captured="currentItem.all_fees_captured"
        :from="from"
        :actual-deposit="currentItem.actual_deposit"
        :actual-rate="currentItem.actual_rate"
        :rental-duration-days="currentItem.rental_duration_days"
      />

      <!-- Rating Card -->
      <RentalViewRatingCard :from="from" :item="currentItem" :rental-id="rentalId" />
    </div>
  </div>
</template>
