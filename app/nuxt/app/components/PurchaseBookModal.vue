<script setup lang="ts">
import { ref, shallowRef, computed, watch } from 'vue'
import { useAddressAutocomplete } from '~/composables/useAddressAutocomplete'
import { useCreatePurchase } from '~/composables/useCreatePurchase'
import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'
import VueTimepicker from 'vue3-timepicker'
import 'vue3-timepicker/dist/VueTimepicker.css'

const { createPurchase, loading, error } = useCreatePurchase()

const df = new DateFormatter('en-US', { dateStyle: 'medium' })

const meetupDateCalendar = shallowRef<CalendarDate | null>(null)

const now = new Date()
const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000)
const minDate = new CalendarDate(tomorrow.getFullYear(), tomorrow.getMonth() + 1, tomorrow.getDate())

const formattedDate = computed(() => {
  if (!meetupDateCalendar.value) return ''
  return df.format(meetupDateCalendar.value.toDate(getLocalTimeZone()))
})

watch(meetupDateCalendar, (val) => {
  if (val && val < minDate) {
    meetupDateCalendar.value = minDate
  }
  meetupDate.value = val ? val.toString() : null
})

const LOCATIONIQ_API_KEY = import.meta.env.VITE_LOCATIONIQ_API_KEY

const meetupAddress = ref('')
const { 
  addressQuery: meetupAddressQuery, 
  suggestions: meetupSuggestions, 
  fetchSuggestions: fetchMeetupSuggestions, 
  selectSuggestion 
} = useAddressAutocomplete(LOCATIONIQ_API_KEY)

const meetupDate = ref<string | null>(null)
const meetupStartTime = ref<{ HH: string, mm: string } | string | null>(null)
const meetupEndTime = ref<{ HH: string, mm: string } | string | null>(null)
const timeError = ref('')

const props = defineProps<{
  isOpenPurchaseBookModal: boolean
  bookId: string
  bookTitle?: string
  bookAuthor?: string
  purchasePrice?: number
  currentWalletBalance?: number
  purchaseExists: boolean
  reserved_amount?: number
}>()

const emit = defineEmits<{
  (e: 'update:openPurchaseBookModal', value: boolean): void
  (e: 'purchase-success'): void
  (e: 'update:purchaseExists', value: boolean): void
}>()

const isOpenPurchaseBookModal = computed({
  get: () => props.isOpenPurchaseBookModal,
  set: (val: boolean) => emit('update:openPurchaseBookModal', val)
})

const availableBalance = computed(() => {
  const balance = props.currentWalletBalance ?? 0
  const reserved = props.reserved_amount ?? 0
  return balance - reserved
})

const hasInsufficientFunds = computed(() => {
  const price = props.purchasePrice ?? 0
  return price > availableBalance.value
})

function onMeetupInput(event: Event) {
  const target = event.target as HTMLInputElement
  if (!target.value) {
    meetupSuggestions.value = []
    return
  }
  fetchMeetupSuggestions()
}

function handleSelectMeetupSuggestion(item: any) {
  selectSuggestion(item, meetupAddress)
  meetupAddressQuery.value = item.display_name
  meetupAddress.value = item.display_name
  meetupSuggestions.value = []
  const input = document.querySelector<HTMLInputElement>('input[v-model="meetupAddressQuery"]')
  input?.blur()
}

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
    timeError.value = '' 
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

watch([meetupStartTime, meetupEndTime], validateTimeWindow)

watch(() => props.isOpenPurchaseBookModal, (isOpen) => {
  if (isOpen) {
    isSending.value = false
    timeError.value = ''
  }
})

const isSending = ref(false)

async function sendPurchase() {
  validateTimeWindow()
  
  if (isSending.value || !!timeError.value || hasInsufficientFunds.value) {
    return
  }

  if (!meetupDate.value || !meetupAddressQuery.value || !meetupStartTime.value || !meetupEndTime.value) {
    return
  }

  isSending.value = true

  try {
    const rawStart = getTimeValue(meetupStartTime.value)
    const rawEnd = getTimeValue(meetupEndTime.value)

    const startStr = formatTimeObj(rawStart)
    const endStr = formatTimeObj(rawEnd)

    if (!startStr || !endStr) {
      timeError.value = 'Please select valid start and end times'
      isSending.value = false
      return 
    }

    await createPurchase({
      book_id: props.bookId, 
      total_buy_cost: props.purchasePrice!,
      meetup_location: meetupAddressQuery.value,
      meetup_date: meetupDate.value,
      meetup_time_window: `${startStr} - ${endStr}`,
    })

    emit('update:purchaseExists', true)
    emit('purchase-success')
    
    isOpenPurchaseBookModal.value = false
    
  } catch (err) {
    console.error(err)
    isSending.value = false
  } 
}
</script>

<template>
  <UModal v-model:open="isOpenPurchaseBookModal" :ui="{ content: 'max-w-lg' }" :dismissible="true">
    <template #header>
      <h2 class="text-2xl font-semibold">Buy {{ props.bookTitle }}</h2>
    </template>

    <template #body>
      <div class="p-4 bg-surface-hover space-y-3 rounded-sm">
        <p class="font-semibold text-base">Purchase Details</p>
        <div class="flex items-center justify-between text-sm text-base">
          <span>Book:</span>
          <span>{{ props.bookTitle }}</span>
        </div>
        <div class="flex items-center justify-between text-sm text-base">
          <span>Author:</span>
          <span>{{ props.bookAuthor }}</span>
        </div>
        <USeparator orientation="horizontal" class="my-2 bg-slate-400" />
        
          <div class="flex items-center justify-between font-semibold text-base" :class="{'text-red-500': hasInsufficientFunds}">
          <span>Total Cost:</span>
          <div class="flex items-center gap-1">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5" :class="hasInsufficientFunds ? 'text-red-500' : 'text-accent'"/>
            <span>{{ props.purchasePrice }}</span>
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
              ({{ props.currentWalletBalance }} total - {{ props.reserved_amount }} reserved)
            </span>
          </div>
        </div>
        </div>
        <div v-if="hasInsufficientFunds" class="flex items-center gap-2 mt-2 p-2 bg-red-50 dark:bg-red-900/20 rounded border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-sm">
          <Icon name="i-heroicons-exclamation-circle" class="w-5 h-5 shrink-0" />
          <span>
            Insufficient available funds.
          </span>
        </div>
      <div class="mt-4">
        <p class="font-semibold text-base">Meetup Location</p>
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
        <div class="flex gap-2 mt-1">
           <VueTimepicker v-model="meetupStartTime" @change="validateTimeWindow" format="HH:mm" :use12-hour="false" placeholder="Start Time" />
           <VueTimepicker v-model="meetupEndTime" @change="validateTimeWindow" format="HH:mm" :use12-hour="false" placeholder="End Time" />
        </div>
        <p v-if="timeError" class="text-red-500 text-sm mt-1">{{ timeError }}</p>
      </div>

      <div class="flex justify-end gap-3 mt-6">
        <UButton 
          @click="isOpenPurchaseBookModal = false" 
          class="bg-slate-300 hover:bg-slate-400 text-black dark:bg-slate-400 dark:hover:bg-slate-500 px-4 py-2 rounded"
        >
          <p>Cancel</p> 
        </UButton>
        <UButton 
          @click.stop.prevent="sendPurchase"
          class="bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-4 py-2 rounded disabled:bg-slate-600 disabled:dark:bg-slate-500 disabled:cursor-not-allowed"
          :disabled="!!timeError || !meetupStartTime || !meetupEndTime || !meetupDate || !meetupAddressQuery || loading || hasInsufficientFunds || isSending"
        >
          <p v-if="!loading && !isSending">Confirm Purchase</p>
          <p v-else>Processing...</p>
        </UButton>
      </div>
    </template>
  </UModal>
</template>
