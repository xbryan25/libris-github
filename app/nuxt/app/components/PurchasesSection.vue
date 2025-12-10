<script setup lang="ts">
import PurchaseCard from './PurchaseCard.vue';
import SaleCard from './SaleCard.vue';
import { useUserSales } from '~/composables/useUserSales';
import { useUserPurchases } from '~/composables/useUserPurchases';

interface Props {
  activeTab: 'selling' | 'buying';
}

defineProps<Props>();

const {
  purchases,
  loading: purchasesLoading,
  error: purchasesError,
  fetchUserPurchases,
} = useUserPurchases();
const { sales, loading: salesLoading, error: salesError, fetchUserSales } = useUserSales();

onMounted(() => {
  fetchUserPurchases();
  fetchUserSales();
});
</script>

<template>
  <div class="w-full bg-background mb-6">
    <div v-if="activeTab === 'selling'">
      <!-- Selling (Sales) content -->
      <div v-if="salesLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your sales...</p>
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
            <p class="text-muted mt-4 text-lg">No active sales</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <SaleCard v-for="sale in sales" :key="sale.purchase_id" :sale="sale" />
      </div>
    </div>

    <div v-else>
      <!-- Buying (Purchases) content -->
      <div v-if="purchasesLoading" class="bg-surface rounded-lg p-6 w-full border border-base">
        <div class="flex justify-center items-center">
          <div class="text-center">
            <UIcon name="lucide:loader-2" class="w-8 h-8 text-muted mx-auto animate-spin" />
            <p class="text-muted mt-4 text-lg">Loading your purchases...</p>
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
            <p class="text-muted mt-4 text-lg">No active purchases</p>
          </div>
        </div>
      </div>

      <div v-else class="space-y-4">
        <PurchaseCard
          v-for="purchase in purchases"
          :key="purchase.purchase_id"
          :purchase="purchase"
        />
      </div>
    </div>
  </div>
</template>
