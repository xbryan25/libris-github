<script setup lang="ts">
import RentalHistoryCard from './RentalHistoryCard.vue';
import LendHistoryCard from './LendHistoryCard.vue';

interface Props {
  activeTab: 'lending' | 'renting';
  sortBy: string;
  sortOrder: string;
  cardsPerPage: number;
}

const props = defineProps<Props>();

const {
  rentals,
  loading: rentalsLoading,
  error: rentalsError,
  fetchUserCompletedRentals,
} = useUserRentals();

const {
  completedRentalsCount,
  loading: rentalsCountLoading,
  fetchUserCompletedRentalsCount,
} = useUserRentalsCount();

const {
  lendings,
  loading: lendingsLoading,
  error: lendingsError,
  fetchUserCompletedLendings,
} = useUserLendings();

const {
  completedLendingsCount,
  loading: lendingsCountLoading,
  fetchUserCompletedLendingsCount,
} = useUserLendingsCount();

const pageNumber = ref(1);

watch(
  [() => props.sortBy, () => props.sortOrder, () => props.cardsPerPage, pageNumber],
  async (newValues) => {
    if (props.activeTab === 'renting') {
      console.log('does it even reach here??');
      await fetchUserCompletedRentals(newValues[0], newValues[1], newValues[2], pageNumber.value);
    } else {
      await fetchUserCompletedLendings(newValues[0], newValues[1], newValues[2], pageNumber.value);
    }
  },
);

watch(
  () => props.activeTab,
  async (newVal) => {
    pageNumber.value = 1;

    if (newVal === 'renting') {
      await fetchUserCompletedRentals(
        props.sortBy,
        props.sortOrder,
        props.cardsPerPage,
        pageNumber.value,
      );
    } else {
      await fetchUserCompletedLendings(
        props.sortBy,
        props.sortOrder,
        props.cardsPerPage,
        pageNumber.value,
      );
    }
  },
);

onMounted(async () => {
  // Get count during mount, as it won't change while user is in this page
  await fetchUserCompletedRentalsCount();
  await fetchUserCompletedLendingsCount();

  if (props.activeTab === 'renting') {
    await fetchUserCompletedRentals(
      props.sortBy,
      props.sortOrder,
      props.cardsPerPage,
      pageNumber.value,
    );
  } else {
    await fetchUserCompletedLendings(
      props.sortBy,
      props.sortOrder,
      props.cardsPerPage,
      pageNumber.value,
    );
  }
});
</script>

<template>
  <div class="w-full bg-background mb-6">
    <div v-if="activeTab === 'lending'">
      <!-- Lending content -->
      <div v-if="lendingsLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your past lendings...</p>
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
            <p class="text-muted mt-4 text-lg">No past lendings yet...</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <LendHistoryCard v-for="lending in lendings" :key="lending.rental_id" :lending="lending" />

        <UPagination
          v-if="!lendingsCountLoading"
          v-model:page="pageNumber"
          :items-per-page="cardsPerPage"
          :total="completedLendingsCount"
          class="w-full flex justify-center"
        />
      </div>
    </div>

    <div v-else>
      <!-- Renting content -->
      <div v-if="rentalsLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your past rentals...</p>
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
            <p class="text-muted mt-4 text-lg">No past rentals yet...</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <RentalHistoryCard v-for="rental in rentals" :key="rental.rental_id" :rental="rental" />

        <UPagination
          v-if="!rentalsCountLoading"
          v-model:page="pageNumber"
          :items-per-page="cardsPerPage"
          :total="completedRentalsCount"
          class="w-full flex justify-center"
        />
      </div>
    </div>
  </div>
</template>
