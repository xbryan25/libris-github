<script setup lang="ts">
interface Props {
  from: string;
  rentalId: string;
  timeWindow?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['approval-success']);

const isApprovalModalOpen = ref(false);
const toast = useToast(); // Assuming you're using Nuxt UI toast

const handleCancelRequest = () => {
  console.log('Cancel request');
  // Add your cancel logic here
}

const handleApproveClick = () => {
  isApprovalModalOpen.value = true;
}

const handleRejectRental = () => {
  console.log('Reject rental');
  // Add your reject logic here
}

const handleApprovalSuccess = () => {
  // Show success message
  toast.add({
    title: 'Success',
    description: 'Rental approved successfully!',
    icon: 'i-lucide-check-circle',
  });
  
  emit('approval-success');
}
</script>

<template>
  <!-- For Rental: Waiting for approval -->
  <div v-if="from === 'rental'" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
    <div class="flex items-start gap-3">
      <Icon name="lucide:info" class="w-5 h-5 text-yellow-600 mt-0.5" />
      <div class="flex-1">
        <p class="text-yellow-800 font-medium">Request Pending: Please wait for the request to be approved by the owner.</p>
      </div>
    </div>
    <button 
      @click="handleCancelRequest"
      class="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
    >
      Cancel Request
    </button>
  </div>

  <!-- For Lending: Action Required -->
  <div v-else-if="from === 'lending'" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
    <div class="flex items-start gap-3">
      <Icon name="lucide:info" class="w-5 h-5 text-blue-600 mt-0.5" />
      <div class="flex-1">
        <p class="text-blue-900 font-medium"><strong>Action Required:</strong> A renter wants to borrow your book. Please approve or reject this request.</p>
      </div>
    </div>
    <div class="flex gap-3 mt-4">
      <button 
        @click="handleApproveClick"
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 cursor-pointer"
      >
        <Icon name="lucide:check" class="w-4 h-4" />
        Approve Rental
      </button>
      <button 
        @click="handleRejectRental"
        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 cursor-pointer"
      >
        <Icon name="lucide:x" class="w-4 h-4" />
        Reject Rental
      </button>
    </div>

    <!-- Approval Modal Component -->
    <RentalApprovalModal
      v-model="isApprovalModalOpen"
      :rental-id="rentalId"
      @success="handleApprovalSuccess"
    />
  </div>
</template>