<script setup lang="ts">
import auth from '~/middleware/auth';
import { useUserPurchases, type Purchase } from '~/composables/useUserPurchases';
import { useUserSales, type Sale } from '~/composables/useUserSales';
import PurchaseCompleteCard from '~/components/PurchaseCompleteCard.vue';
import PurchaseRatingCard from '~/components/PurchaseRatingCard.vue';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const router = useRouter();
const purchaseid = route.params.purchaseid as string;
const from = route.query.from as string;

const { purchases, fetchUserPurchases } = useUserPurchases();
const { sales, fetchUserSales } = useUserSales();

const currentItem = ref<Purchase | Sale | null>(null);
const loading = ref(true);
const showRating = ref(false);

const currentStatus = computed(() => {
  if (!currentItem.value) return '';
  if (showRating.value) return 'rate_user';
  return currentItem.value.purchase_status;
});

const fetchPurchaseData = async () => {
  loading.value = true;
  try {
    if (from === 'purchase') {
      await fetchUserPurchases();
      currentItem.value = purchases.value.find(p => p.purchase_id === purchaseid) || null;
    } else if (from === 'sale') {
      await fetchUserSales();
      currentItem.value = sales.value.find(s => s.purchase_id === purchaseid) || null;
    }
  } catch (error) {
    console.error('Error fetching purchase data:', error);
  } finally {
    loading.value = false;
  }
}

const handleApprovalSuccess = async () => {
  await fetchPurchaseData();
}

const handleShowRating = () => {
  showRating.value = true;
}

const handleBackToComplete = () => {
  showRating.value = false;
}

onMounted(() => {
  fetchPurchaseData();
});
</script>

<template>
  <div class="min-h-screen w-full pt-4 pb-6 px-4 md:px-8 lg:px-15">
    <!-- Header -->
    <div class="mb-6">
      <button 
        @click="router.back()"
        class="flex items-center gap-2 text-base pt-4 pb-4 hover:text-foreground mb-4 cursor-pointer"
      >
        <Icon name="lucide:arrow-left" class="w-5 h-5" />
        <span>Back to Purchases</span>
      </button>
      
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
      <PurchaseBookInfoCard 
        v-if="currentItem.purchase_status !== 'completed'"
        :item="currentItem" 
        :from="from" 
      />

      <!-- Progress Stepper -->
      <PurchaseProgressStepper 
        v-if="currentItem.purchase_status !== 'pending'" 
        :status="currentStatus" 
        :from="from" 
      />

      <!-- Dates & Meetup Grid -->
      <PurchaseDetailsGrid 
        v-if="currentItem.purchase_status !== 'completed'"
        :item="currentItem"
        :from="from"
      />

      <!-- Cost Card -->
      <PurchaseCostCard 
        v-if="currentItem.purchase_status !== 'completed'"
        :cost="currentItem.cost"
        :all-fees-captured="currentItem.all_fees_captured"
        :from="from"
      />

      <!-- Complete Card or Rating Card -->
      <template v-if="currentItem.purchase_status === 'completed'">
        <PurchaseCompleteCard
          v-if="!showRating"
          :status="currentItem.purchase_status"
          :from="from"
          :item="currentItem"
          @show-rating="handleShowRating"
        />
        
        <PurchaseRatingCard
          v-else
          :from="from"
          :item="currentItem"
          :purchase-id="purchaseid"
          @back-to-complete="handleBackToComplete"
        />
      </template>

      <!-- Confirmation Cards -->
      <PurchaseConfirmationCard
        v-if="currentItem.purchase_status === 'approved' || currentItem.purchase_status === 'awaiting_pickup_confirmation'"
        :status="currentItem.purchase_status"
        :from="from"
        :purchase-id="purchaseid"
        :meetup-date="currentItem.meetup_date"
        :meetup-time="currentItem.meetup_time"
        :user-confirmed-pickup="currentItem.user_confirmed_pickup"
        :owner-confirmed-pickup="currentItem.owner_confirmed_pickup"
        @refresh="fetchPurchaseData"
      />

      <!-- Pending Actions -->
      <PurchasePendingActions
        v-if="currentItem.purchase_status === 'pending'"
        :from="from"
        :purchase-id="purchaseid"
        @approval-success="handleApprovalSuccess"
        @refresh="fetchPurchaseData"
      />
    </div>
  </div>
</template>