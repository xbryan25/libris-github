<script setup lang="ts">


const props = defineProps<{
  isOpenRentBookModal: boolean
  bookTitle?: string
  dailyRentPrice?: number
  securityDeposit?: number
}>()

const emit = defineEmits<{
  (e: 'update:openRentBookModal', value: boolean): void
}>()

const isOpenRentBookModal = computed({
  get: () => props.isOpenRentBookModal,
  set: (val: boolean) => emit('update:openRentBookModal', val)
})
const rentOptions = [
  '1 day',
  '3 days',
  '5 days',
  '7 days',
  '14 days',
  'Custom'
]
const selected = ref('')
const customDays = ref<number | null>(null)
const finalDays = ref<number | null>(null)
const meetupDate = ref<string | null>(null)
const meetupTime = ref('')
const timeError = ref('')

function validateTimeWindow() {
  const cleaned = meetupTime.value.replace(/\s+/g, ' ').trim()
  const pattern = /^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)\s*-\s*(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)$/i
  if (!pattern.test(cleaned)) {
    timeError.value = 'Invalid format. Example: 10:30 AM - 12:00 PM'
  } else {
    timeError.value = ''
  }
}

watch(meetupTime, validateTimeWindow)

watch(selected, (value) => {
  if (value !== 'Custom') {
    customDays.value = null
    finalDays.value = Number(value.split(' ')[0])
  }
})

watch(customDays, (value) => {
  if (selected.value === 'Custom' && value) {
    finalDays.value = value
  }
})
const totalCost = computed(() => {
  if (!finalDays.value) return 0
  const rent = props.dailyRentPrice ?? 0
  const deposit = props.securityDeposit ?? 0
  return rent * finalDays.value + deposit
})

</script>

<template>
  <UModal v-model:open="isOpenRentBookModal" :ui="{ content: 'max-w-lg' }" :dismissible="true">
    <template #header>
      <h2 class="text-2xl font-semibold">Rent {{ props.bookTitle }}</h2>
    </template>

    <template #body>
        <div class="p-4 bg-surface-hover space-y-3 rounded-sm">
          <p class="font-semibold text-base">Rental Details</p>

          <div class="flex items-center justify-between text-sm text-base">
            <span>Daily Rate:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>{{ props.dailyRentPrice }}/day</span>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm text-base">
            <span>Security Deposit:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>{{props.securityDeposit}}</span>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm text-base">
            <span>Rental Period:</span>
            <span>{{ finalDays?? '-'}}</span>
          </div>

          <USeparator orientation="horizontal" class="my-2 bg-slate-400" />

          <div class="flex items-center justify-between font-semibold text-base">
            <span>Total Cost:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>{{ totalCost }}</span>
            </div>
          </div>
        </div>
        <p class="font-semibold text-base mt-4">Rental Duration</p>
        <USelect v-model="selected" :items="rentOptions" class="w-full mt-2" />
        <div v-if="selected === 'Custom'" class="mt-2">
          <p class="text-sm text-gray-600">Enter custom number of days:</p>
          <UInput 
            type="number"
            v-model="customDays"
            min="1"
            placeholder="e.g., 12"
            class="mt-1 w-full"
          />
        </div>
        <div class="mt-4">
          <p class="font-semibold text-base">Meetup Date</p>
          <UInput 
            type="date" 
            v-model="meetupDate" 
            class="mt-1 w-full" 
          />
        </div>
        <div class="mt-4">
          <p class="font-semibold text-base">Meetup Time Window</p>
          <UInput
            v-model="meetupTime"
            placeholder="10:30 AM - 12:00 PM"
            @blur="validateTimeWindow"
            class="mt-1 w-full"
          />
          <p v-if="timeError" class="text-red-500 text-sm mt-1">{{ timeError }}</p>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <UButton @click="isOpenRentBookModal = false" class="bg-slate-300 hover:bg-slate-400 text-black dark:bg-slate-400 dark:hover:bg-slate-500 px-4 py-2 rounded">
          <p>Cancel</p> 
          </UButton>
          <UButton :disabled="!!timeError || !meetupTime || !finalDays || !meetupDate" class="bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-4 py-2 rounded">
          <p>Send Rental Request</p> 
          </UButton>
        </div>
  </template>
  </UModal>
</template>
