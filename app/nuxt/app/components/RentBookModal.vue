<script setup lang="ts">
import { ref, shallowRef, computed, watch } from 'vue'
import { useAddressAutocomplete } from '~/composables/useAddressAutocomplete';
import { useCreateRental } from '~/composables/useCreateRental';
import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'
import VueTimepicker from 'vue3-timepicker'
import 'vue3-timepicker/dist/VueTimepicker.css'

const { createRental, loading, error } = useCreateRental()

const df = new DateFormatter('en-US', { dateStyle: 'medium' })

const meetupDateCalendar = shallowRef<CalendarDate | null>(null)

const now = new Date()
const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000)
const minDate = new CalendarDate(tomorrow.getFullYear(), tomorrow.getMonth() + 1, tomorrow.getDate())

const formattedDate = computed(() => {
  if (!meetupDateCalendar.value) return ''
  return df.format(meetupDateCalendar.value.toDate(getLocalTimeZone()))
})


const LOCATIONIQ_API_KEY = import.meta.env.VITE_LOCATIONIQ_API_KEY;
const meetupAddress = ref('') 
const { 
  addressQuery: meetupAddressQuery, 
  suggestions: meetupSuggestions, 
  fetchSuggestions: fetchMeetupSuggestions, 
  selectSuggestion: selectMeetupSuggestion 
} = useAddressAutocomplete(LOCATIONIQ_API_KEY)

const props = defineProps<{
  isOpenRentBookModal: boolean
  bookId: string
  bookTitle?: string
  dailyRentPrice?: number
  securityDeposit?: number
  rentalExists: boolean
  currentWalletBalance?: number
  reservedAmount?: number
}>()


const emit = defineEmits<{
  (e: 'update:openRentBookModal', value: boolean): void
  (e: 'rental-success'): void
  (e: 'update:rentalExists', value: boolean): void
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
const meetupStartTime = ref<string | { HH: string, mm: string } | null>(null)
const meetupEndTime = ref<string | { HH: string, mm: string } | null>(null)
const timeError = ref('')


function getTimeValue(val: any): string {
  if (!val) return ''
  if (typeof val === 'string') return val
  if (typeof val === 'object' && val.HH && val.mm) return `${val.HH}:${val.mm}`
  return ''
}

function validateTimeWindow() {
  const startStr = getTimeValue(meetupStartTime.value)
  const endStr = getTimeValue(meetupEndTime.value)

  if (!startStr || !endStr) {
    return
  }

  const startDate = new Date(`1970-01-01T${startStr}:00`)
  const endDate = new Date(`1970-01-01T${endStr}:00`)

  if (endDate <= startDate) {
    timeError.value = 'End time must be later than start time'
  } else {
    timeError.value = ''
  }
}

watch([meetupStartTime, meetupEndTime], () => {
  validateTimeWindow()
})

function handleSelectMeetupSuggestion(item: any) {
  selectMeetupSuggestion(item, meetupAddress)
  meetupAddressQuery.value = item.display_name
  meetupAddress.value = item.display_name
  meetupSuggestions.value = [] 
}

watch(selected, (value) => {
  if (value !== 'Custom') {
    customDays.value = null
    finalDays.value = Number(value.split(' ')[0])
  }
})

function preventDecimal(event: KeyboardEvent) {
  if (['.', 'e', '-', '+'].includes(event.key)) {
    event.preventDefault()
  }
}

watch(customDays, (value) => {
  if (selected.value === 'Custom' && value) {
    finalDays.value = Math.floor(value)
  }
})

watch(meetupDateCalendar, (val) => {
  if (val && val < minDate) {
    meetupDateCalendar.value = minDate
  }
  meetupDate.value = val ? df.format(val.toDate(getLocalTimeZone())) : null
})

function onMeetupInput(event: Event) {
  const target = event.target as HTMLInputElement
  if (!target.value) {
    meetupSuggestions.value = [] 
    return
  }
  fetchMeetupSuggestions()
}

const totalCost = computed(() => {
  if (!finalDays.value) return 0
  const rent = props.dailyRentPrice ?? 0
  const deposit = props.securityDeposit ?? 0
  return rent * finalDays.value + deposit
})

const availableBalance = computed(() => {
  const balance = props.currentWalletBalance ?? 0
  const reserved = props.reservedAmount ?? 0
  return balance - reserved
})

const hasInsufficientFunds = computed(() => {
  return totalCost.value > availableBalance.value
})

function formatTimeObj(time: string | null | undefined) {
  if (!time) return ''
  const [hStr, mStr] = time.split(':')
  if (!hStr || !mStr) return ''
  
  let h = parseInt(hStr)
  const m = parseInt(mStr)
  const ampm = h >= 12 ? 'PM' : 'AM'
  
  if (h === 0) h = 12
  if (h > 12) h -= 12
  
  return `${h}:${m.toString().padStart(2, '0')} ${ampm}`
}

const isSendingRental = ref(false)

async function sendRental() {
  validateTimeWindow()

  if (isSendingRental.value || !!timeError.value) return

  if (isSendingRental.value || !!timeError.value || hasInsufficientFunds.value) return

  isSendingRental.value = true

  try {
    const rawStart = getTimeValue(meetupStartTime.value)
    const rawEnd = getTimeValue(meetupEndTime.value)

    const startStr = formatTimeObj(rawStart)
    const endStr = formatTimeObj(rawEnd)

    if (!startStr || !endStr) {
      timeError.value = 'Please select valid start and end times'
      return 
    }

    await createRental({
      book_id: props.bookId,
      total_rent_cost: totalCost.value,
      rental_duration_days: finalDays.value!,
      meetup_time_window: `${startStr} - ${endStr}`, 
      meetup_location: meetupAddressQuery.value,
      meetup_date: meetupDate.value!
    })

    emit('update:rentalExists', true)
    emit('rental-success')
    isOpenRentBookModal.value = false
  } catch (err) {
    console.error(err)
  } finally {
    isSendingRental.value = false
  }
}
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
            <div class="flex items-center gap-1" :class="{'text-red-500': hasInsufficientFunds}">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent" :class="hasInsufficientFunds ? 'text-red-500' : 'text-accent'"/>
              <span>{{ totalCost }}</span>
            </div>
          </div>
          <div class="flex items-start justify-between font-semibold text-base mt-2">
            <span class="mt-0.5">Available Balance:</span> 

            <div class="flex flex-col items-end">
              <div class="flex items-center gap-1">
                <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
                <span>{{ availableBalance }}</span>
              </div>
              <span class="text-xs text-gray-500 font-normal">
                ({{ props.currentWalletBalance }} current balance - {{ props.reservedAmount }} reserved)
              </span>
            </div>
          </div>
          <div v-if="hasInsufficientFunds" class="flex items-center gap-2 mt-2 p-2 bg-red-50 dark:bg-red-900/20 rounded border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-sm">
            <Icon name="i-heroicons-exclamation-circle" class="w-5 h-5 shrink-0" />
            <span>Insufficient wallet balance for this rental duration.</span>
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
            @keydown="preventDecimal"
          />
        </div>
        <div class="mt-4">
          <p class="font-semibold text-base mt-4">Meetup Location</p>
          <div class="relative w-full">
            <UInput
              v-model="meetupAddressQuery"
              placeholder="Enter meetup location..."
              class="mt-1 w-full"
              @input="onMeetupInput"
            />
            <ul
              v-if="meetupSuggestions.length"
              class="absolute z-50 bg-white dark:bg-zinc-800 border border-gray-300 dark:border-zinc-700 rounded w-full max-h-60 overflow-auto shadow-lg"
            >
              <li
                v-for="(item, i) in meetupSuggestions"
                :key="i"
                @click="handleSelectMeetupSuggestion(item)"
                class="p-2 cursor-pointer hover:bg-gray-200 dark:hover:bg-zinc-700"
              >
                {{ item.display_name }}
              </li>
            </ul>
          </div>
        </div>
        <div class="mt-4">
          <p class="font-semibold text-base">Meetup Date</p>
          <UPopover>
            <UButton color="neutral" variant="subtle" icon="i-lucide-calendar">
              {{ formattedDate || 'Select a date' }}
            </UButton>

            <template #content>
              <UCalendar v-model="meetupDateCalendar" class="p-2" :minValue="minDate" />
            </template>
          </UPopover>
        </div>
        <div class="mt-4">
          <p class="font-semibold text-base">Meetup Time Window</p>
          <div class="flex gap-2">
            <VueTimepicker v-model="meetupStartTime" @change="validateTimeWindow" format="HH:mm" :use12-hour="false" placeholder="Start Time" />
            <VueTimepicker v-model="meetupEndTime" @change="validateTimeWindow" format="HH:mm" :use12-hour="false" placeholder="End Time" />
          </div>
          <p v-if="timeError" class="text-red-500 text-sm mt-1">{{ timeError }}</p>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <UButton @click="isOpenRentBookModal = false" class="bg-slate-300 hover:bg-slate-400 text-black dark:bg-slate-400 dark:hover:bg-slate-500 px-4 py-2 rounded">
          <p>Cancel</p> 
          </UButton>
          <UButton
            @click="sendRental"
            :disabled="!!timeError || !meetupStartTime || !meetupEndTime || !finalDays || !meetupDate || !meetupAddressQuery || loading || hasInsufficientFunds"
            class="bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-4 py-2 rounded disabled:bg-slate-600 disabled:dark:bg-slate-500 disabled:cursor-not-allowed"
          >
            <p v-if="!loading">Send Rental Request</p> 
            <p v-else>Sending...</p>
          </UButton>
        </div>
  </template>
  </UModal>
</template>
