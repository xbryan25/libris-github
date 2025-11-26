<script setup lang="ts">
interface Props {
  status: string;
  from: string;
  meetupDate: string;
  meetupTime: string;
  rentEndDate: string;
}

const props = defineProps<Props>();

const showPickupConfirmation = computed(() => {
  return props.status === 'awaiting_pickup_confirmation';
});

const showReturnConfirmation = computed(() => {
  return props.status === 'awaiting_return_confirmation';
});
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
    <button 
      v-if="from === 'rental'"
      class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
    >
      <Icon name="lucide:check" class="w-5 h-5" />
      Confirm Received Book
    </button>
    <button 
      v-else-if="from === 'lending'"
      class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
    >
      <Icon name="lucide:check" class="w-5 h-5" />
      Confirm Delivered Book
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
    <button 
      v-if="from === 'rental'"
      class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
    >
      <Icon name="lucide:check" class="w-5 h-5" />
      Confirm Returned Book
    </button>
    <button 
      v-else-if="from === 'lending'"
      class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer"
    >
      <Icon name="lucide:check" class="w-5 h-5" />
      Confirm Received Back Book
    </button>
  </div>
</template>