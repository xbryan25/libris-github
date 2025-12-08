<script setup lang="ts">
import { useCompletedPurchaseRating } from '~/composables/useCompletedPurchaseRating';

interface Props {
  purchaseId: string;
}

const props = defineProps<Props>();

const { getCompletedPurchaseRatings, loading } = useCompletedPurchaseRating();

const givenRating = ref(0);
const givenComment = ref('');

const receivedRating = ref(0);
const receivedComment = ref('');

onMounted(async () => {
  const data = await getCompletedPurchaseRatings(props.purchaseId);

  if (data) {
    givenRating.value = data.givenRating;
    givenComment.value = data.givenComment;

    receivedRating.value = data.receivedRating;
    receivedComment.value = data.receivedComment;
  }

  console.log(data);
});
</script>

<template>
  <div class="space-y-6">
    <!-- Rating Card -->
    <div v-if="!loading" class="bg-surface rounded-lg border border-base p-8 flex gap-10">
      <div class="flex-1">
        <div class="text-center mb-3">
          <div class="flex justify-center gap-2">
            <Icon name="lucide:star" class="w-16 h-16 text-amber-500 mb-4" />
            <Icon name="lucide:arrow-big-up" class="w-16 h-16 text-amber-500 mb-4" />
          </div>

          <h2 class="text-2xl font-bold mb-2">Rating Given</h2>
        </div>

        <!-- Star Rating -->
        <div>
          <div class="flex justify-center items-center gap-3">
            <Icon
              v-for="star in [1, 2, 3, 4, 5]"
              :key="star"
              name="lucide:star"
              :class="[
                'w-14 h-14 transition-all duration-200',
                star <= givenRating ? 'text-amber-400 fill-amber-400' : 'text-gray-300',
              ]"
            />
          </div>
        </div>

        <div v-if="givenComment !== ''" class="mt-5 p-5 bg-background rounded-xl">
          <p class="text-justify">{{ givenComment }}</p>
        </div>
      </div>

      <div class="flex-1">
        <div class="text-center mb-3">
          <div class="flex justify-center gap-2">
            <Icon name="lucide:star" class="w-16 h-16 text-amber-500 mb-4" />
            <Icon name="lucide:arrow-big-down" class="w-16 h-16 text-amber-500 mb-4" />
          </div>
          <h2 class="text-2xl font-bold mb-2">Rating Received</h2>
        </div>

        <!-- Star Rating -->
        <div>
          <div class="flex justify-center items-center gap-3">
            <Icon
              v-for="star in [1, 2, 3, 4, 5]"
              :key="star"
              name="lucide:star"
              :class="[
                'w-14 h-14 transition-all duration-200',
                star <= receivedRating ? 'text-amber-400 fill-amber-400' : 'text-gray-300',
              ]"
            />
          </div>
        </div>

        <div v-if="receivedComment !== ''" class="mt-5 p-5 bg-background rounded-xl">
          <p class="text-justify">{{ receivedComment }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
