<script setup lang="ts">
interface Props {
  from: string;
  purchaseId: string;
  timeWindow?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['approval-success', 'rejection-success', 'cancel-success', 'refresh']);

const isApprovalModalOpen = ref(false);
const isRejectModalOpen = ref(false);
const isCancelModalOpen = ref(false);
const toast = useToast(); 

const handleCancelClick = () => {
  isCancelModalOpen.value = true;
}

const handleApproveClick = () => {
  isApprovalModalOpen.value = true;
}

const handleRejectClick = () => {
  isRejectModalOpen.value = true;
}

const handleApprovalSuccess = () => {
  toast.add({
    title: 'Success',
    description: 'Purchase approved successfully!',
    icon: 'i-lucide-check-circle',
  });
  
  emit('approval-success');
}

const handleApprovalConflict = () => {
  toast.add({
    title: 'Purchase Status Changed',
    description: 'This book has been approved for another buyer. Refreshing...',
    icon: 'i-lucide-info',
  });
  
  emit('refresh');
}

const handleRejectionSuccess = () => {
  toast.add({
    title: 'Purchase Rejected',
    description: 'The purchase request has been rejected.',
    icon: 'i-lucide-x-circle',
  });
  
  emit('rejection-success');
  navigateTo('/purchases');
}

const handleCancelSuccess = () => {
  toast.add({
    title: 'Request Cancelled',
    description: 'Your purchase request has been cancelled.',
    icon: 'i-lucide-x-circle',
  });
  
  emit('cancel-success');
  navigateTo('/purchases');
}
</script>

<template>
  <!-- For Purchase: Waiting for approval -->
  <div v-if="from === 'purchase'" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
    <div class="flex items-start gap-3">
      <Icon name="lucide:info" class="w-5 h-5 text-yellow-600 mt-0.5" />
      <div class="flex-1">
        <p class="text-yellow-800 font-medium">Request Pending: Please wait for the request to be approved by the seller.</p>
      </div>
    </div>
    <button 
      @click="handleCancelClick"
      class="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors cursor-pointer"
    >
      Cancel Request
    </button>

    <!-- Cancel Modal Component -->
    <PurchaseCancelModal
      v-model="isCancelModalOpen"
      :purchase-id="purchaseId"
      @success="handleCancelSuccess"
    />
  </div>

  <!-- For Sale: Action Required -->
  <div v-else-if="from === 'sale'" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
    <div class="flex items-start gap-3">
      <Icon name="lucide:info" class="w-5 h-5 text-blue-600 mt-0.5" />
      <div class="flex-1">
        <p class="text-blue-900 font-medium"><strong>Action Required:</strong> A buyer wants to purchase your book. Please approve or reject this request.</p>
      </div>
    </div>
    <div class="flex gap-3 mt-4">
      <button 
        @click="handleApproveClick"
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 cursor-pointer"
      >
        <Icon name="lucide:check" class="w-4 h-4" />
        Approve Purchase
      </button>
      <button 
        @click="handleRejectClick"
        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 cursor-pointer"
      >
        <Icon name="lucide:x" class="w-4 h-4" />
        Reject Purchase
      </button>
    </div>

    <!-- Approval Modal Component -->
    <PurchaseApprovalModal
      v-model="isApprovalModalOpen"
      :purchase-id="purchaseId"
      @success="handleApprovalSuccess"
      @conflict="handleApprovalConflict"
    />

    <!-- Rejection Modal Component -->
    <PurchaseRejectModal
      v-model="isRejectModalOpen"
      :purchase-id="purchaseId"
      @success="handleRejectionSuccess"
    />
  </div>
</template>