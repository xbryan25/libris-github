<script setup lang="ts">
import { useUserLendings } from '~/composables/useUserLendings';
import { useRentalActions } from '~/composables/useRentalActions';

interface Props {
  rentalId: string;
}

const props = defineProps<Props>();

const isOpen = defineModel<boolean>();
const emit = defineEmits(['success']);

const { fetchUserLendings } = useUserLendings();
const { rejectRental, loading: submitting } = useRentalActions();

const rejectionForm = reactive({
  reason: '',
});

const submitError = ref('');

const predefinedReasons = [
  'Book is no longer available',
  'Cannot meet at the requested time/location',
  'Changed my mind about lending'
];

const handleReasonSelect = (reason: string) => {
  rejectionForm.reason = reason;
};

const handleSubmit = async () => {
  submitError.value = '';
  
  if (!rejectionForm.reason) {
    submitError.value = 'Please select a reason for rejection';
    return;
  }

  // Call the API to reject the rental with the reason
  const result = await rejectRental(
    props.rentalId,
    rejectionForm.reason
  );

  if (result.success) {
    emit('success');
    
    isOpen.value = false;
    
    await fetchUserLendings();
  } else {
    submitError.value = result.error || 'Failed to reject rental';
  }
};

// Reset form when modal closes
watch(isOpen, (newValue) => {
  if (!newValue) {
    rejectionForm.reason = '';
    submitError.value = '';
  }
});
</script>

<template>
  <UModal v-model:open="isOpen">
    <template #header>
      <h2 class="text-2xl font-semibold">Reject Rental Request</h2>
    </template>

    <template #body>
      <div class="space-y-4">
        <p class="text-muted">Please provide a reason for rejecting this rental request. This will help the renter understand your decision.</p>
        
        <!-- Error Alert -->
        <div v-if="submitError" class="bg-red-50 border border-red-200 rounded-lg p-3 dark:bg-red-900/20 dark:border-red-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:alert-circle" class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-red-900 dark:text-red-300">
              {{ submitError }}
            </p>
          </div>
        </div>

        <!-- Warning Box -->
        <div class="bg-amber-50 border border-amber-200 rounded-lg p-3 dark:bg-amber-900/20 dark:border-amber-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:alert-triangle" class="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-amber-900 dark:text-amber-300">
              This action cannot be undone. The renter will be notified of the rejection.
            </p>
          </div>
        </div>

        <!-- Predefined Reasons -->
        <div>
          <label class="block text-sm font-medium mb-2">
            Select a Reason <span class="text-red-500">*</span>
          </label>
          <div class="space-y-2">
            <button
              v-for="reason in predefinedReasons"
              :key="reason"
              type="button"
              @click="handleReasonSelect(reason)"
              :class="[
                'w-full text-left px-4 py-3 rounded-lg border transition-all',
                rejectionForm.reason === reason
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-900 dark:text-blue-300'
                  : 'border-gray-300 dark:border-gray-600 hover:border-blue-300 dark:hover:border-blue-700',
                submitting ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
              ]"
              :disabled="submitting"
            >
              <div class="flex items-center gap-3">
                <div 
                  :class="[
                    'w-5 h-5 rounded-full border-2 flex items-center justify-center',
                    rejectionForm.reason === reason
                      ? 'border-blue-500'
                      : 'border-gray-300 dark:border-gray-600'
                  ]"
                >
                  <div 
                    v-if="rejectionForm.reason === reason"
                    class="w-3 h-3 rounded-full bg-blue-500"
                  />
                </div>
                <span class="text-sm">{{ reason }}</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Info Box -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 dark:bg-blue-900/20 dark:border-blue-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:info" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-blue-900 dark:text-blue-300">
              The rental entry will be deleted and reserved funds will be released back to the renter. The renter will receive a notification with your reason for rejection.
            </p>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <div class="w-full flex justify-end gap-3">
        <UButton
          variant="ghost"
          @click="isOpen = false"
          :disabled="submitting"
          class="hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
        >
          Cancel
        </UButton>
        <UButton
          @click="handleSubmit"
          :disabled="!rejectionForm.reason || submitting"
          :loading="submitting"
          class="text-white bg-red-600 hover:bg-red-700 focus:ring-red-500 disabled:bg-red-400 disabled:cursor-not-allowed cursor-pointer"
        >
          <Icon v-if="!submitting" name="lucide:x" class="w-4 h-4 mr-2" />
          {{ submitting ? 'Rejecting...' : 'Reject Request' }}
        </UButton>
      </div>
    </template>
  </UModal>
</template>