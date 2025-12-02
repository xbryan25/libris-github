<script setup lang="ts">
import PurchaseHistoryCard from './PurchaseHistoryCard.vue';
import SellHistoryCard from './SellHistoryCard.vue';

interface Props {
  activeTab: 'selling' | 'buying';
  sortBy: string;
  sortOrder: string;
  cardsPerPage: number;
}

const props = defineProps<Props>();

// const {
//   rentals,
//   loading: rentalsLoading,
//   error: rentalsError,
//   fetchUserCompletedRentals,
// } = useUserRentals();

// const {
//   completedRentalsCount,
//   loading: rentalsCountLoading,
//   fetchUserCompletedRentalsCount,
// } = useUserRentalsCount();

// const {
//   lendings,
//   loading: lendingsLoading,
//   error: lendingsError,
//   fetchUserCompletedLendings,
// } = useUserLendings();

// const {
//   completedLendingsCount,
//   loading: lendingsCountLoading,
//   fetchUserCompletedLendingsCount,
// } = useUserLendingsCount();

const pageNumber = ref(1);

watch(
  [() => props.sortBy, () => props.sortOrder, () => props.cardsPerPage, pageNumber],
  async (newValues) => {
    if (props.activeTab === 'buying') {
      console.log('does it even reach here??');
      // await fetchUserCompletedRentals(newValues[0], newValues[1], newValues[2], pageNumber.value);
    } else {
      // await fetchUserCompletedLendings(newValues[0], newValues[1], newValues[2], pageNumber.value);
      console.log('uncomment later');
    }
  },
);

watch(
  () => props.activeTab,
  async (newVal) => {
    pageNumber.value = 1;

    if (newVal === 'buying') {
      // await fetchUserCompletedRentals(
      //   props.sortBy,
      //   props.sortOrder,
      //   props.cardsPerPage,
      //   pageNumber.value,
      // );

      console.log('uncomment later');
    } else {
      // await fetchUserCompletedLendings(
      //   props.sortBy,
      //   props.sortOrder,
      //   props.cardsPerPage,
      //   pageNumber.value,
      // );

      console.log('uncomment later');
    }
  },
);

onMounted(async () => {
  // Get count during mount, as it won't change while user is in this page

  // await fetchUserCompletedRentalsCount();
  // await fetchUserCompletedLendingsCount();

  console.log('uncomment later');

  if (props.activeTab === 'buying') {
    // await fetchUserCompletedRentals(
    //   props.sortBy,
    //   props.sortOrder,
    //   props.cardsPerPage,
    //   pageNumber.value,
    // );

    console.log('uncomment later');
  } else {
    // await fetchUserCompletedLendings(
    //   props.sortBy,
    //   props.sortOrder,
    //   props.cardsPerPage,
    //   pageNumber.value,
    // );

    console.log('uncomment later');
  }
});
</script>

<template>
  <div class="w-full bg-background">
    <div v-if="activeTab === 'selling'">
      <!-- Lending content -->
      <div v-if="salesLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your past sales...</p>
          </div>
        </div>
      </div>

      <div v-else-if="salesError" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:alert-circle" class="w-16 h-16 text-red-500 mx-auto" />
            <p class="text-red-500 mt-4 text-lg">{{ salesError }}</p>
          </div>
        </div>
      </div>

      <div
        v-else-if="sales.length === 0"
        class="bg-surface rounded-lg p-6 w-full border border-base"
      >
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="bytesize:book" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">No past sales yet...</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <SellHistoryCard v-for="sale in sales" :key="sale.rental_id" :sale="sale" />

        <UPagination
          v-if="!salesCountLoading"
          v-model:page="pageNumber"
          :items-per-page="cardsPerPage"
          :total="completedSalesCount"
          class="w-full flex justify-center"
        />
      </div>
    </div>

    <div v-else>
      <!-- Renting content -->
      <div v-if="purchasesLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your past purchases...</p>
          </div>
        </div>
      </div>

      <div v-else-if="purchasesError" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:alert-circle" class="w-16 h-16 text-red-500 mx-auto" />
            <p class="text-red-500 mt-4 text-lg">{{ purchasesError }}</p>
          </div>
        </div>
      </div>

      <div
        v-else-if="purchases.length === 0"
        class="bg-surface rounded-lg p-6 w-full border border-base"
      >
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="bytesize:book" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">No past purchases yet...</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <PurchaseHistoryCard
          v-for="purchase in purchases"
          :key="purchase.rental_id"
          :purchase="purchase"
        />

        <UPagination
          v-if="!purchasesCountLoading"
          v-model:page="pageNumber"
          :items-per-page="cardsPerPage"
          :total="completedPurchasesCount"
          class="w-full flex justify-center"
        />
      </div>
    </div>
  </div>
</template>
