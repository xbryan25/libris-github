<script setup lang="ts">
interface Props {
  from: string;
  rentEndDate: string;
}

const props = defineProps<Props>();

const daysRemaining = computed(() => {
  if (!props.rentEndDate) return 0;
  
  const endDate = new Date(props.rentEndDate);
  const now = new Date();
  const diffTime = endDate.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  return diffDays > 0 ? diffDays : 0;
});
</script>

<template>
  <div class="bg-purple-50 border border-purple-200 rounded-lg p-5">
    <div class="flex items-start gap-3">
      <Icon name="lucide:book-open" class="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
      <div class="flex-1">
        <p class="text-purple-900 font-medium mb-2">
          {{ from === 'rental' ? 'You are currently renting this book.' : 'This book is currently being rented.' }}
        </p>
        <p class="text-sm text-purple-800">
          <strong>{{ daysRemaining }}</strong> day(s) remaining until return date.
        </p>
      </div>
    </div>
  </div>
</template>