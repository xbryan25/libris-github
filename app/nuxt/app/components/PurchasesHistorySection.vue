<script setup lang="ts">
import { useUserPurchasesCount } from '~/composables/useUserPurchasesCount';
import { useUserSalesCount } from '~/composables/useUserSalesCount';
import PurchaseHistoryCard from './PurchaseHistoryCard.vue';
import SaleHistoryCard from './SaleHistoryCard.vue';

interface Props {
  activeTab: 'selling' | 'buying';
  sortOrder: string;
  cardsPerPage: number;
}

const props = defineProps<Props>();

const {
  purchases,
  loading: purchasesLoading,
  error: purchasesError,
  fetchUserCompletedPurchases,
} = useUserPurchases();

const {
  completedPurchasesCount,
  loading: purchasesCountLoading,
  fetchUserCompletedPurchasesCount,
} = useUserPurchasesCount();

const { sales, loading: salesLoading, error: salesError, fetchUserCompletedSales } = useUserSales();

const {
  completedSalesCount,
  loading: salesCountLoading,
  fetchUserCompletedSalesCount,
} = useUserSalesCount();

const pageNumber = ref(1);

watch([() => props.sortOrder, () => props.cardsPerPage, pageNumber], async (newValues) => {
  if (props.activeTab === 'buying') {
    await fetchUserCompletedPurchases(newValues[0], newValues[1], pageNumber.value);
  } else {
    await fetchUserCompletedSales(newValues[0], newValues[1], pageNumber.value);
  }
});

watch(
  () => props.activeTab,
  async (newVal) => {
    pageNumber.value = 1;

    if (newVal === 'buying') {
      await fetchUserCompletedPurchases(props.sortOrder, props.cardsPerPage, pageNumber.value);
    } else {
      await fetchUserCompletedSales(props.sortOrder, props.cardsPerPage, pageNumber.value);
    }
  },
);

onMounted(async () => {
  // Get count during mount, as it won't change while user is in this page

  await fetchUserCompletedPurchasesCount();
  await fetchUserCompletedSalesCount();

  if (props.activeTab === 'buying') {
    await fetchUserCompletedPurchases(props.sortOrder, props.cardsPerPage, pageNumber.value);
  } else {
    await fetchUserCompletedSales(props.sortOrder, props.cardsPerPage, pageNumber.value);
  }
});
</script>

<template>
  <div class="w-full bg-background mb-6">
    <div v-if="activeTab === 'selling'">
      <!-- Sell content -->
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
        <SaleHistoryCard v-for="sale in sales" :key="sale.purchase_id" :sale="sale" />

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
      <!-- Purchase content -->
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
          :key="purchase.purchase_id"
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
