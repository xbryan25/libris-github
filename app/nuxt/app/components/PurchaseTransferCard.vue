<script setup lang="ts">
import { useTransferDecision } from '~/composables/useTransferDecision';

interface Props {
  purchaseId: string;
  from: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['refresh']);

const toast = useToast();
const { submitTransferDecision, loading: submitting } = useTransferDecision();
const selectedOption = ref<'yes' | 'no' | null>(null);

const handleTransferDecision = async () => {
  if (!selectedOption.value) {
    toast.add({
      title: 'Selection Required',
      description: 'Please select an option before continuing.',
      icon: 'i-lucide-alert-circle',
    });
    return;
  }

  const transferOwnership = selectedOption.value === 'yes';
  
  const result = await submitTransferDecision(props.purchaseId, transferOwnership);
  
  if (result.success) {
    toast.add({
      title: 'Decision Submitted',
      description: transferOwnership
        ? 'Book ownership will be transferred to you.' 
        : 'You have declined the ownership transfer.',
      icon: 'i-lucide-check-circle',
    });

    // Refresh the purchase data
    emit('refresh');
  } else {
    toast.add({
      title: 'Submission Failed',
      description: result.error || 'Failed to submit your decision. Please try again.',
      icon: 'i-lucide-x-circle',
    });
  }
};

const selectOption = (option: 'yes' | 'no') => {
  selectedOption.value = option;
};
</script>

<template>
  <div class="bg-surface rounded-lg border border-base p-6">
    <div class="text-center mb-6">
      <Icon name="lucide:refresh-cw" class="w-16 h-16 text-purple-500 mx-auto mb-4" />
      <h2 class="text-2xl font-bold mb-2">Transfer Book Ownership?</h2>
      <p class="text-muted">
        Would you like to transfer the ownership of this book to your account? 
        This will add the book to your library.
      </p>
    </div>

    <!-- Transfer Options -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <!-- Yes Option -->
      <button
        @click="selectOption('yes')"
        :class="[
          'p-6 rounded-lg border-2 transition-all cursor-pointer',
          selectedOption === 'yes'
            ? 'border-green-500 bg-green-500 text-white'
            : 'border-green-500 bg-green-500/20 hover:bg-green-500/30 text-green-700 dark:text-green-300'
        ]"
      >
        <div class="flex flex-col items-center gap-3">
          <Icon 
            name="lucide:check-circle" 
            :class="[
              'w-12 h-12',
              selectedOption === 'yes' ? 'text-white' : 'text-green-600 dark:text-green-400'
            ]"
          />
          <div>
            <h3 class="font-bold text-lg mb-1">Yes, Transfer Ownership</h3>
            <p :class="['text-sm', selectedOption === 'yes' ? 'text-white/90' : 'text-green-700 dark:text-green-300']">
              Add this book to my library
            </p>
          </div>
        </div>
      </button>

      <!-- No Option -->
      <button
        @click="selectOption('no')"
        :class="[
          'p-6 rounded-lg border-2 transition-all cursor-pointer',
          selectedOption === 'no'
            ? 'border-red-500 bg-red-500 text-white'
            : 'border-red-500 bg-red-500/20 hover:bg-red-500/30 text-red-700 dark:text-red-300'
        ]"
      >
        <div class="flex flex-col items-center gap-3">
          <Icon 
            name="lucide:x-circle" 
            :class="[
              'w-12 h-12',
              selectedOption === 'no' ? 'text-white' : 'text-red-600 dark:text-red-400'
            ]"
          />
          <div>
            <h3 class="font-bold text-lg mb-1">No, Don't Transfer</h3>
            <p :class="['text-sm', selectedOption === 'no' ? 'text-white/90' : 'text-red-700 dark:text-red-300']">
              Keep the book but not added to your library
            </p>
          </div>
        </div>
      </button>
    </div>

    <!-- Info Box -->
    <div class="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
      <div class="flex items-start gap-3">
        <Icon name="lucide:info" class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
        <div class="text-sm">
          <p class="font-medium text-blue-900 dark:text-blue-100 mb-1">
            What does this mean?
          </p>
          <ul class="text-blue-800 dark:text-blue-200 space-y-1 list-disc list-inside">
            <li>If you select <strong>Yes</strong>, the book will be added to your library and you can list it for rent or sale.</li>
            <li>If you select <strong>No</strong>, the transaction will complete, the book will still be transferred to you, but not listed in your library.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="flex justify-center">
      <button
        @click="handleTransferDecision"
        :disabled="!selectedOption || submitting"
        :class="[
          'px-8 py-3 rounded-lg font-medium transition-colors inline-flex items-center gap-2 cursor-pointer',
          !selectedOption || submitting
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-accent hover:bg-accent/90 text-white'
        ]"
      >
        <Icon v-if="submitting" name="lucide:loader-2" class="w-5 h-5 animate-spin" />
        <Icon v-else name="lucide:arrow-right" class="w-5 h-5" />
        {{ submitting ? 'Submitting...' : 'Continue' }}
      </button>
    </div>
  </div>
</template>