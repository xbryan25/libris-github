<script setup lang="ts">
interface Props {
  status: string;
  from: string;
  meetupDate: string;
  meetupTime: string;
  rentEndDate: string;
}

const props = defineProps<Props>();

const isWithinOneHourOfMeetup = computed(() => {
  if (props.status !== 'approved') return false;
  if (!props.meetupDate || !props.meetupTime) return false;
  
  const meetupDateTime = new Date(`${props.meetupDate} ${props.meetupTime}`);
  const now = new Date();
  const oneHourBeforeMeetup = new Date(meetupDateTime.getTime() - 60 * 60 * 1000);
  
  return now >= oneHourBeforeMeetup && now <= meetupDateTime;
});

const isWithinOneHourOfReturn = computed(() => {
  if (props.status !== 'ongoing') return false;
  if (!props.rentEndDate) return false;
  
  const returnTime = props.meetupTime || '18:00';
  const returnDateTime = new Date(`${props.rentEndDate} ${returnTime}`);
  const now = new Date();
  const oneHourBeforeReturn = new Date(returnDateTime.getTime() - 60 * 60 * 1000);
  
  return now >= oneHourBeforeReturn && now <= returnDateTime;
});
</script>

<template>
  <!-- Approved Status Confirmation -->
  <div v-if="status === 'approved'">
    <!-- Warning Message -->
    <div v-if="!isWithinOneHourOfMeetup" class="bg-blue-50 border border-blue-200 rounded-lg p-5">
      <div class="flex items-start gap-3">
        <Icon name="lucide:clock" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
        <p class="text-sm text-blue-900">
          A confirmation button will appear 1 hour before the meetup time to confirm the book handoff.
        </p>
      </div>
    </div>

    <!-- Confirmation Button -->
    <div v-else class="bg-blue-50 border-2 border-blue-300 rounded-lg p-5">
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
  </div>

  <!-- Ongoing Status Confirmation -->
  <div v-if="status === 'ongoing'">
    <!-- Warning Message -->
    <div v-if="!isWithinOneHourOfReturn" class="bg-blue-50 border border-blue-200 rounded-lg p-5">
      <div class="flex items-start gap-3">
        <Icon name="lucide:clock" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
        <p class="text-sm text-blue-900">
          A confirmation button will appear 1 hour before the return date to confirm the book return.
        </p>
      </div>
    </div>

    <!-- Confirmation Button -->
    <div v-else class="bg-blue-50 border-2 border-blue-300 rounded-lg p-5">
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
  </div>
</template>