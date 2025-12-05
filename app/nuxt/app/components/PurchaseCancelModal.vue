<script setup lang="ts">
import { useUserPurchases } from '~/composables/useUserPurchases';
import { usePurchaseActions } from '~/composables/usePurchaseActions';

interface Props {
  purchaseId: string;
}

const props = defineProps<Props>();

const isOpen = defineModel<boolean>();
const emit = defineEmits(['success']);

const { fetchUserPurchases } = useUserPurchases();
const { cancelPurchase, loading: submitting } = usePurchaseActions();

const submitError = ref('');

const handleSubmit = async () => {
  submitError.value = '';

  const result = await cancelPurchase(props.purchaseId);

  if (result.success) {
    emit('success');
    
    isOpen.value = false;
    
    await fetchUserPurchases();
  } else {
    submitError.value = result.error || 'Failed to cancel purchase';
  }
};

watch(isOpen, (newValue) => {
  if (!newValue) {
    submitError.value = '';
  }
});
</script>

<template>
  <UModal v-model:open="isOpen">
    <template #header>
      <h2 class="text-2xl font-semibold">Cancel Purchase Request</h2>
    </template>

    <template #body>
      <div class="space-y-4">
        <!-- Error Alert -->
        <div v-if="submitError" class="bg-red-50 border border-red-200 rounded-lg p-3 dark:bg-red-900/20 dark:border-red-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:alert-circle" class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-red-900 dark:text-red-300">
              {{ submitError }}
            </p>
          </div>
        </div>

        <!-- Confirmation Message -->
        <p class="text-base text-foreground">
          Are you sure you want to cancel this purchase request? Your reserved funds will be released back to your wallet.
        </p>

        <!-- Info Box -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 dark:bg-blue-900/20 dark:border-blue-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:info" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-blue-900 dark:text-blue-300">
              This action cannot be undone. The purchase request will be deleted and the book seller will be notified.
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
          Keep Request
        </UButton>
        <UButton
          @click="handleSubmit"
          :disabled="submitting"
          :loading="submitting"
          class="text-white bg-red-600 hover:bg-red-700 focus:ring-red-500 disabled:bg-red-400 disabled:cursor-not-allowed cursor-pointer"
        >
          <Icon v-if="!submitting" name="lucide:x" class="w-4 h-4 mr-2" />
          {{ submitting ? 'Cancelling...' : 'Cancel Request' }}
        </UButton>
      </div>
    </template>
  </UModal>
</template>