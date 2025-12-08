<script setup lang="ts">
import auth from '~/middleware/auth';
import { useUserRentals, type Rental } from '~/composables/useUserRentals';
import { useUserLendings, type Lending } from '~/composables/useUserLendings';
import RentalCompleteCard from '~/components/RentalCompleteCard.vue';
import RentalRatingCard from '~/components/RentalRatingCard.vue';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const router = useRouter();
const rentalId = route.params.rentalId as string;
const from = route.query.from as string;

const { rentals, fetchUserRentals } = useUserRentals();
const { lendings, fetchUserLendings } = useUserLendings();

const currentItem = ref<Rental | Lending | null>(null);
const loading = ref(true);
const showRating = ref(false);

const currentStatus = computed(() => {
  if (!currentItem.value) return '';
  if (showRating.value) return 'rate_user';
  return currentItem.value.rent_status;
});

const fetchRentalData = async () => {
  loading.value = true;
  try {
    if (from === 'rental') {
      await fetchUserRentals();
      currentItem.value = rentals.value.find((r) => r.rental_id === rentalId) || null;
    } else if (from === 'lending') {
      await fetchUserLendings();
      currentItem.value = lendings.value.find((l) => l.rental_id === rentalId) || null;
    }
  } catch (error) {
    console.error('Error fetching rental data:', error);
  } finally {
    loading.value = false;
  }
};

const handleApprovalSuccess = async () => {
  await fetchRentalData();
};

const handleShowRating = () => {
  showRating.value = true;
};

const handleBackToComplete = () => {
  showRating.value = false;
};

onMounted(() => {
  fetchRentalData();
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
        <span>Back to Rentals</span>
      </button>

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
      <RentalBookInfoCard
        v-if="currentItem.rent_status !== 'completed'"
        :item="currentItem"
        :from="from"
      />

      <!-- Progress Stepper (Show for all statuses, use computed status) -->
      <RentalProgressStepper
        v-if="currentItem.rent_status !== 'pending'"
        :status="currentStatus"
        :from="from"
      />

      <!-- Active Rental Alert -->
      <RentalActiveAlert
        v-if="currentItem.rent_status === 'ongoing'"
        :from="from"
        :rent-end-date="currentItem.rent_end_date"
      />

      <!-- Dates & Meetup Grid -->
      <RentalDetailsGrid
        v-if="currentItem.rent_status !== 'completed'"
        :item="currentItem"
        :from="from"
      />

      <!-- Cost Card -->
      <RentalCostCard
        v-if="currentItem.rent_status !== 'completed'"
        :cost="currentItem.cost"
        :all-fees-captured="currentItem.all_fees_captured"
        :from="from"
        :actual-deposit="currentItem.actual_deposit"
        :actual-rate="currentItem.actual_rate"
        :rental-duration-days="currentItem.rental_duration_days"
      />

      <!-- Complete Card or Rating Card (Toggle) -->
      <template v-if="currentItem.rent_status === 'completed'">
        <RentalCompleteCard
          v-if="!showRating"
          :status="currentItem.rent_status"
          :actual-deposit="currentItem.actual_deposit"
          :from="from"
          :item="currentItem"
          @show-rating="handleShowRating"
        />

        <RentalRatingCard
          v-else
          :from="from"
          :item="currentItem"
          :rental-id="rentalId"
          @back-to-complete="handleBackToComplete"
        />
      </template>

      <!-- Confirmation Cards (for approved and ongoing) -->
      <RentalConfirmationCard
        v-if="
          currentItem.rent_status === 'approved' ||
          currentItem.rent_status === 'ongoing' ||
          currentItem.rent_status === 'awaiting_pickup_confirmation' ||
          currentItem.rent_status === 'awaiting_return_confirmation'
        "
        :status="currentItem.rent_status"
        :from="from"
        :rental-id="rentalId"
        :meetup-date="currentItem.meetup_date"
        :meetup-time="currentItem.meetup_time"
        :rent-end-date="currentItem.rent_end_date"
        :user-confirmed-pickup="currentItem.user_confirmed_pickup"
        :owner-confirmed-pickup="currentItem.owner_confirmed_pickup"
        :user-confirmed-return="currentItem.user_confirmed_return"
        :owner-confirmed-return="currentItem.owner_confirmed_return"
        @refresh="fetchRentalData"
      />

      <!-- Pending Actions -->
      <RentalPendingActions
        v-if="currentItem.rent_status === 'pending'"
        :from="from"
        :rental-id="rentalId"
        @approval-success="handleApprovalSuccess"
        @refresh="fetchRentalData"
      />
    </div>
  </div>
</template>
