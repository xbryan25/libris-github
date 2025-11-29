<script setup lang="ts">
import type { Rental } from '~/composables/useUserRentals';
import type { Lending } from '~/composables/useUserLendings';
import Rating from 'primevue/rating';

interface Props {
  from: string;
  item: Rental | Lending;
  rentalId: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['back-to-complete']);

const rating = ref(0);
const review = ref('');
const submitting = ref(false);

const userName = computed(() => {
  return props.from === 'rental' 
    ? (props.item as Rental).from 
    : (props.item as Lending).to;
});

const handleSubmit = async () => {
  if (rating.value === 0) {
    return;
  }
  
  submitting.value = true;
  
  // TODO hi husnie: CHANGE THIS TO A PROPER API CALL. THIS FOR TEST ONLY
  try {
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('Rating submitted:', { rating: rating.value, review: review.value });
    navigateTo('/rentals');
  } catch (error) {
    console.error('Error submitting rating:', error);
  } finally {
    submitting.value = false;
  }
};

const handleBack = () => {
  emit('back-to-complete');
};
</script>

<template>
  <div class="space-y-6">
    <!-- Rating Card -->
    <div class="bg-surface rounded-lg border border-base p-8">
      <div class="text-center mb-6">
        <Icon name="lucide:star" class="w-16 h-16 text-amber-500 mx-auto mb-4" />
        <h2 class="text-2xl font-bold mb-2">Rate Your Experience</h2>
        <p class="text-muted">How was your experience {{ from === 'rental' ? 'renting from' : 'lending to' }} {{ userName }}?</p>
      </div>

      <!-- Star Rating -->
      <div class="flex justify-center mb-6">
        <Rating v-model="rating" :stars="5" :cancel="false" class="text-4xl" />
      </div>

      <!-- Review Text Area -->
      <div class="mb-6">
        <label class="block text-sm font-medium mb-2">
          Share your thoughts (Optional)
        </label>
        <textarea
          v-model="review"
          placeholder="Tell us about your experience..."
          rows="4"
          class="w-full px-4 py-3 border border-base rounded-lg focus:outline-none focus:ring-2 focus:ring-accent bg-background"
        ></textarea>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3 justify-center">
        <button
          @click="handleBack"
          class="px-6 py-3 border border-base rounded-lg font-medium hover:bg-surface transition-colors cursor-pointer"
        >
          Back
        </button>
        <button
          @click="handleSubmit"
          :disabled="rating === 0 || submitting"
          :class="[
            'px-6 py-3 rounded-lg font-medium transition-colors inline-flex items-center gap-2 cursor-pointer',
            rating === 0 || submitting
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-accent hover:bg-accent/90 text-white'
          ]"
        >
          <Icon v-if="submitting" name="lucide:loader-2" class="w-5 h-5 animate-spin" />
          <Icon v-else name="lucide:send" class="w-5 h-5" />
          {{ submitting ? 'Submitting...' : 'Submit Rating' }}
        </button>
      </div>
    </div>
  </div>
</template>