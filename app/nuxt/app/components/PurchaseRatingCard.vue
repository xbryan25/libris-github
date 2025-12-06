<script setup lang="ts">
import type { Purchase } from '~/composables/useUserPurchases';
import type { Sale } from '~/composables/useUserSales';
import { useRating } from '~/composables/useRating';

interface Props {
  from: string;
  item: Purchase | Sale;
  purchaseId: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['back-to-complete']);

const { submitRating, loading: ratingLoading } = useRating();
const toast = useToast();

const rating = ref(0);
const review = ref('');
const submitting = ref(false);

const userName = computed(() => {
  return props.from === 'purchase' 
    ? (props.item as Purchase).from 
    : (props.item as Sale).to;
});

const selectRating = (value: number) => {
  rating.value = value;
  console.log('Rating selected:', value);
};

const handleSubmit = async () => {
  console.log('Submitting rating:', rating.value);
  
  if (rating.value === 0) {
    toast.add({
      title: 'Rating Required',
      description: 'Please select a rating before submitting.',
      icon: 'i-lucide-alert-circle',
    });
    return;
  }
  
  submitting.value = true;
  
  try {
    const result = await submitRating(
      props.purchaseId,
      rating.value,
      review.value,
      props.from as 'purchase' | 'sale'
    );
    
    if (result.success) {
      toast.add({
        title: 'Rating Submitted',
        description: 'Thank you for your feedback!',
        icon: 'i-lucide-check-circle',
      });
      navigateTo('/purchases');
    } else {
      toast.add({
        title: 'Submission Failed',
        description: result.error || 'Failed to submit rating',
        icon: 'i-lucide-x-circle',
      });
    }
  } catch (error) {
    console.error('Error submitting rating:', error);
    toast.add({
      title: 'Submission Failed',
      description: 'An error occurred while submitting your rating',
      icon: 'i-lucide-x-circle',
    });
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
        <p class="text-muted">How was your experience {{ from === 'purchase' ? 'buying from' : 'selling to' }} {{ userName }}?</p>
      </div>

      <!-- Star Rating -->
      <div class="mb-6">
        <div class="flex justify-center items-center gap-3 mb-2">
          <button
            v-for="star in [1, 2, 3, 4, 5]"
            :key="star"
            @click="selectRating(star)"
            type="button"
            class="cursor-pointer focus:outline-none rounded-full p-1 transition-all duration-200 hover:scale-125"
          >
            <Icon
              name="lucide:star"
              :class="[
                'w-14 h-14 transition-all duration-200',
                star <= rating ? 'text-amber-400 fill-amber-400' : 'text-gray-300'
              ]"
            />
          </button>
        </div>
        <p class="text-center text-sm text-muted">
          {{ rating === 0 ? 'Click to rate' : `${rating} out of 5 stars` }}
        </p>
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