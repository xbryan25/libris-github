<script setup lang="ts">
import { useUserSales } from '~/composables/useUserSales';
import { usePurchaseActions } from '~/composables/usePurchaseActions';

interface Props {
  purchaseId: string;
}

const props = defineProps<Props>();

const isOpen = defineModel<boolean>();
const emit = defineEmits(['submit', 'success']);

const { sales, fetchUserSales } = useUserSales();
const { approvePurchase, loading: submitting } = usePurchaseActions();

const approvalForm = reactive({
  meetupTime: '',
});

const validationError = ref('');
const submitError = ref('');

const currentSale = computed(() => {
  return sales.value.find(sale => sale.purchase_id === props.purchaseId);
});

const timeWindow = computed(() => {
  return currentSale.value?.meetup_time_window || '';
});

const meetupLocation = computed(() => {
  return currentSale.value?.meetup_location || '';
});

// Parse time window string (e.g., "10:00 AM - 1:00 PM")
const parseTimeWindow = (timeWindowStr: string) => {
  if (!timeWindowStr) return null;
  
  const parts = timeWindowStr.split('-').map(s => s.trim());
  if (parts.length !== 2) return null;
  
  const parseTime = (timeStr: string) => {
    const match = timeStr.match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i);
    if (!match) return null;
    
    let hours = parseInt(match[1]);
    const minutes = parseInt(match[2]);
    const period = match[3].toUpperCase();
    
    if (period === 'PM' && hours !== 12) hours += 12;
    if (period === 'AM' && hours === 12) hours = 0;
    
    return hours * 60 + minutes; 
  };
  
  return {
    start: parseTime(parts[0]),
    end: parseTime(parts[1])
  };
};

// Validate if selected time is within the time window
const validateTime = () => {
  validationError.value = '';
  
  if (!approvalForm.meetupTime) return true;
  if (!timeWindow.value) return true;
  
  const window = parseTimeWindow(timeWindow.value);
  if (!window || window.start === null || window.end === null) {
    return true;
  }
  
  const [hours, minutes] = approvalForm.meetupTime.split(':').map(Number);
  const selectedMinutes = hours * 60 + minutes;
  
  if (selectedMinutes < window.start || selectedMinutes > window.end) {
    validationError.value = `Time must be between ${timeWindow.value}`;
    return false;
  }
  
  return true;
};

watch(() => approvalForm.meetupTime, () => {
  if (approvalForm.meetupTime) {
    validateTime();
  }
});

const handleSubmit = async () => {
  submitError.value = '';
  
  if (!approvalForm.meetupTime) {
    submitError.value = 'Please fill in the meetup time';
    return;
  }
  
  if (!validateTime()) {
    return;
  }

  const result = await approvePurchase(
    props.purchaseId,
    approvalForm.meetupTime
  );

  if (result.success) {
    emit('submit', {
      purchaseId: props.purchaseId,
      meetupTime: approvalForm.meetupTime,
    });
    
    emit('success');
    
    isOpen.value = false;
    
    await fetchUserSales();
  } else {
    submitError.value = result.error || 'Failed to approve purchase';
  }
};

watch(isOpen, (newValue) => {
  if (!newValue) {
    approvalForm.meetupTime = '';
    validationError.value = '';
    submitError.value = '';
  }
});

watch(isOpen, async (newValue) => {
  if (newValue && sales.value.length === 0) {
    await fetchUserSales();
  }
});
</script>

<template>
  <UModal v-model:open="isOpen">
    <template #header>
      <h2 class="text-2xl font-semibold">Set Meetup Details</h2>
    </template>

    <template #body>
      <div class="space-y-4">
        <p class="text-muted">Please provide the meetup time for the book handoff.</p>
        
        <!-- Error Alert -->
        <div v-if="submitError" class="bg-red-50 border border-red-200 rounded-lg p-3 dark:bg-red-900/20 dark:border-red-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:alert-circle" class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-red-900 dark:text-red-300">
              {{ submitError }}
            </p>
          </div>
        </div>

        <!-- Meetup Location Display -->
        <div v-if="meetupLocation" class="bg-blue-50 border border-blue-200 rounded-lg p-3 dark:bg-blue-900/20 dark:border-blue-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:map-pin" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <p class="text-sm font-medium text-blue-900 dark:text-blue-300">
                Requested Meetup Location
              </p>
              <p class="text-sm text-blue-800 dark:text-blue-400">
                {{ meetupLocation }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- Time Window Display -->
        <div v-if="timeWindow" class="bg-amber-50 border border-amber-200 rounded-lg p-3 dark:bg-amber-900/20 dark:border-amber-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:clock" class="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
            <div>
              <p class="text-sm font-medium text-amber-900 dark:text-amber-300">
                Requested Time Window
              </p>
              <p class="text-sm text-amber-800 dark:text-amber-400">
                {{ timeWindow }}
              </p>
            </div>
          </div>
        </div>

        <!-- Meetup Time -->
        <div>
          <label class="block text-sm font-medium mb-2">
            Meetup Time
            <span v-if="timeWindow" class="text-amber-600 font-normal ml-2">
              *Must be within the requested time window above
            </span>
          </label>
          <input
            v-model="approvalForm.meetupTime"
            type="time"
            :class="[
              'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 bg-white dark:bg-gray-800',
              validationError 
                ? 'border-red-500 focus:ring-red-500' 
                : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
            ]"
            :disabled="submitting"
            required
          />
          <p v-if="validationError" class="text-red-600 text-sm mt-1 flex items-center gap-1">
            <Icon name="lucide:alert-circle" class="w-4 h-4" />
            {{ validationError }}
          </p>
        </div>

        <!-- Info Box -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 dark:bg-blue-900/20 dark:border-blue-800">
          <div class="flex items-start gap-2">
            <Icon name="lucide:info" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-blue-900 dark:text-blue-300">
              The buyer will be notified of the meetup time. You can confirm the book handoff once you meet at the requested location.
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
          color="error"
          :disabled="submitting"
          class="color-red-500 hover:bg-red-100 hover:text-red-600 cursor-pointer"
        >
          Cancel
        </UButton>
        <UButton
          @click="handleSubmit"
          :disabled="!!validationError || submitting"
          :loading="submitting"
          class="text-white bg-green-600 hover:bg-green-700 focus:ring-green-500 cursor-pointer"
        >
          <Icon v-if="!submitting" name="lucide:check" class="w-4 h-4 mr-2" />
          {{ submitting ? 'Approving...' : 'Confirm Approval' }}
        </UButton>
      </div>
    </template>
  </UModal>
</template>