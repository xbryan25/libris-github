<script setup lang="ts">
import auth from '~/middleware/auth';
import { useUserPurchases, type Purchase } from '~/composables/useUserPurchases';
import { useUserSales, type Sale } from '~/composables/useUserSales';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const purchaseId = route.params.purchaseId as string;
const from = route.query.from as string;

const { purchases, fetchUserCompletedPurchase } = useUserPurchases();
const { sales, fetchUserCompletedSale } = useUserSales();

const currentItem = ref<Purchase | Sale | null>(null);
const loading = ref(true);

const fetchPurchaseData = async () => {
  loading.value = true;
  try {
    if (from === 'purchase') {
      await fetchUserCompletedPurchase(purchaseId);
      currentItem.value = purchases.value[0] ?? null;
    } else if (from === 'sale') {
      await fetchUserCompletedSale(purchaseId);
      currentItem.value = sales.value[0] ?? null;
    }
  } catch (error) {
    console.error('Error fetching purchase data:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPurchaseData();
});
</script>

<template>
  <div class="min-h-screen w-full pt-4 pb-6 px-4 md:px-8 lg:px-15">
    <!-- Header -->
    <div class="mb-6">
      <NuxtLink
        :to="`/purchases/history?activeTab=${from === 'purchase' ? 'buying' : 'selling'}`"
        class="flex items-center gap-2 text-base pt-4 pb-4 hover:text-foreground mb-4 cursor-pointer"
      >
        <Icon name="lucide:arrow-left" class="w-5 h-5" />
        <span>Back to {{ from === 'purchase' ? 'Purchases' : 'Sales' }} History</span>
      </NuxtLink>

      <h1 class="font-bold text-3xl flex items-center gap-2 mb-1">
        <Icon
          :name="from === 'purchase' ? 'lucide:trending-down' : 'lucide:trending-up'"
          class="w-8 h-8 text-orange-500"
        />
        {{ from === 'purchase' ? 'Purchase Details' : 'Sale Details' }}
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
          <p class="text-red-500 mt-4 text-lg">Purchase not found</p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Book Info Card -->
      <PurchaseBookInfoCard :item="currentItem" :from="from" :is-completed="true" />

      <!-- Dates & Meetup Grid -->
      <PurchaseDetailsGrid :item="currentItem" :from="from" />

      <!-- Cost Card -->
      <PurchaseCostCard
        :cost="currentItem.cost"
        :all-fees-captured="currentItem.all_fees_captured"
        :from="from"
      />

      <!-- Rating Card -->
      <PurchaseViewRatingCard :from="from" :item="currentItem" :purchase-id="purchaseId" />
    </div>
  </div>
</template>
