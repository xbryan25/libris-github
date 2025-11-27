<script setup lang="ts">
import { useRentalActions } from '~/composables/useRentalActions';

interface Props {
  status: string;
  from: string;
  meetupDate: string;
  meetupTime: string;
  rentEndDate: string;
  rentalId: string;
  userConfirmedPickup: boolean;
  ownerConfirmedPickup: boolean;
  userConfirmedReturn: boolean;
  ownerConfirmedReturn: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['refresh']);

const { confirmPickup, loading } = useRentalActions();
const toast = useToast();

const showPickupConfirmation = computed(() => {
  return props.status === 'awaiting_pickup_confirmation';
});

const showReturnConfirmation = computed(() => {
  return props.status === 'awaiting_return_confirmation';
});

const isPickupConfirmed = computed(() => {
  if (props.from === 'rental') {
    return props.userConfirmedPickup;
  } else {
    return props.ownerConfirmedPickup;
  }
});

const isReturnConfirmed = computed(() => {
  if (props.from === 'rental') {
    return props.userConfirmedReturn;
  } else {
    return props.ownerConfirmedReturn;
  }
});

const handleConfirmPickup = async () => {
  const result = await confirmPickup(props.rentalId);
  
  if (result.success) {
    toast.add({
      title: 'Success',
      description: 'Pickup confirmed!',
      icon: 'i-lucide-check-circle',
    });
    
    // Emit refresh event to parent
    emit('refresh');
  } else {
    toast.add({
      title: 'Error',
      description: result.error || 'Failed to confirm pickup',
      icon: 'i-lucide-alert-circle',
      color: 'red',
    });
  }
};
</script>

<template>
  <!-- Approved Status - Waiting Message -->
  <div v-if="status === 'approved'" class="bg-blue-50 border border-blue-200 rounded-lg p-5">
    <div class="flex items-start gap-3">
      <Icon name="lucide:clock" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
      <p class="text-sm text-blue-900">
        A confirmation button will appear 1 hour before the meetup time to confirm the book handoff.
      </p>
    </div>
  </div>

  <!-- Awaiting Pickup Confirmation Status -->
  <div v-if="showPickupConfirmation" class="bg-blue-50 border-2 border-blue-300 rounded-lg p-5">
    <div class="mb-4 flex items-start gap-3">
      <Icon name="lucide:alert-circle" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
      <p class="text-sm text-blue-900 font-medium">
        Please confirm if you have {{ from === 'rental' ? 'received' : 'delivered' }} the book. Both users must confirm to progress the rental.
      </p>
    </div>

    <!-- Confirmed Status -->
    <div v-if="isPickupConfirmed" class="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
      <div class="flex items-center gap-2">
        <Icon name="lucide:check-circle" class="w-5 h-5 text-green-600" />
        <p class="text-sm font-medium text-green-900">
          ✓ Confirmed. Waiting for other user to confirm...
        </p>
      </div>
    </div>

    <!-- Confirm Button -->
    <button 
      v-if="!isPickupConfirmed"
      @click="handleConfirmPickup"
      :disabled="loading"
      class="w-full bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:cursor-not-allowed"
    >
      <Icon v-if="!loading" name="lucide:check" class="w-5 h-5" />
      <Icon v-else name="lucide:loader-2" class="w-5 h-5 animate-spin" />
      {{ loading ? 'Confirming...' : (from === 'rental' ? 'Confirm Received Book' : 'Confirm Delivered Book') }}
    </button>
  </div>

  <!-- Ongoing Status - Waiting Message -->
  <div v-if="status === 'ongoing'" class="bg-blue-50 border border-blue-200 rounded-lg p-5">
    <div class="flex items-start gap-3">
      <Icon name="lucide:clock" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
      <p class="text-sm text-blue-900">
        A confirmation button will appear 1 hour before the return date to confirm the book return.
      </p>
    </div>
  </div>

  <!-- Awaiting Return Confirmation Status -->
  <div v-if="showReturnConfirmation" class="bg-blue-50 border-2 border-blue-300 rounded-lg p-5">
    <div class="mb-4 flex items-start gap-3">
      <Icon name="lucide:alert-circle" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
      <p class="text-sm text-blue-900 font-medium">
        Please confirm if you have {{ from === 'rental' ? 'returned' : 'received back' }} the book. Both users must confirm to complete the rental.
      </p>
    </div>

    <!-- Confirmed Status for Return -->
    <div v-if="isReturnConfirmed" class="mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
      <div class="flex items-center gap-2">
        <Icon name="lucide:check-circle" class="w-5 h-5 text-green-600" />
        <p class="text-sm font-medium text-green-900">
          ✓ Confirmed. Waiting for other user to confirm...
        </p>
      </div>
    </div>

    <button 
      v-if="!isReturnConfirmed"
      class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
    >
      <Icon name="lucide:check" class="w-5 h-5" />
      {{ from === 'rental' ? 'Confirm Returned Book' : 'Confirm Received Back Book' }}
    </button>
  </div>
</template>