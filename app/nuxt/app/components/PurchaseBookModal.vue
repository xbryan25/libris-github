<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAddressAutocomplete } from '~/composables/useAddressAutocomplete'
import { useCreatePurchase } from '~/composables/useCreatePurchase'

const { createPurchase, loading, error } = useCreatePurchase()

const LOCATIONIQ_API_KEY = import.meta.env.VITE_LOCATIONIQ_API_KEY

const meetupAddress = ref('')
const { 
  addressQuery: meetupAddressQuery, 
  suggestions: meetupSuggestions, 
  fetchSuggestions: fetchMeetupSuggestions, 
  selectSuggestion 
} = useAddressAutocomplete(LOCATIONIQ_API_KEY)

const meetupDate = ref<string | null>(null)
const meetupTimeWindow = ref('')
const timeError = ref('')

const props = defineProps<{
  isOpenPurchaseBookModal: boolean
  bookId: string
  bookTitle?: string
  bookAuthor?: string
  purchasePrice?: number
  currentWalletBalance?: number
  purchaseExists: boolean
}>()

const emit = defineEmits<{
  (e: 'update:openPurchaseBookModal', value: boolean): void
  (e: 'purchase-success'): void
  (e: 'update:rentalExists', value: boolean): void
}>()

const isOpenPurchaseBookModal = computed({
  get: () => props.isOpenPurchaseBookModal,
  set: (val: boolean) => emit('update:openPurchaseBookModal', val)
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

function validateTimeWindow() {
  const cleaned = meetupTimeWindow.value.replace(/\s+/g, ' ').trim()
  const pattern = /^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)\s*-\s*(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)$/i
  if (!pattern.test(cleaned)) {
    timeError.value = 'Invalid format. Example: 10:30 AM - 12:00 PM'
  } else {
    timeError.value = ''
  }
}

watch(meetupTimeWindow, validateTimeWindow)

async function sendPurchase() {
  if (!meetupDate.value || !meetupAddressQuery.value || !!timeError.value || !meetupTimeWindow.value) return

  try {
    await createPurchase({
      book_id: props.bookId, 
      total_buy_cost: props.purchasePrice!,
      meetup_location: meetupAddressQuery.value,
      meetup_date: meetupDate.value,
      meetup_time_window: meetupTimeWindow.value,
    })
    emit('purchase-success')
    isOpenPurchaseBookModal.value = false
  } catch (err) {
    console.error(err)
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
        <div class="flex items-center justify-between font-semibold text-base">
          <span>Total Cost:</span>
          <span>{{ props.purchasePrice }}</span>
        </div>
        <div class="flex items-center justify-between font-semibold text-base">
          <span>Your Balance:</span>
          <span>{{ props.currentWalletBalance }}</span>
        </div>
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
        <UInput 
          type="date" 
          v-model="meetupDate" 
          class="mt-1 w-full" 
        />
      </div>

      <div class="mt-4">
        <p class="font-semibold text-base">Meetup Time Window</p>
        <UInput
          v-model="meetupTimeWindow"
          placeholder="10:30 AM - 12:00 PM"
          @blur="validateTimeWindow"
          class="mt-1 w-full"
        />
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
          @click="sendPurchase"
          class="bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-4 py-2 rounded disabled:bg-slate-600 disabled:dark:bg-slate-500 disabled:cursor-not-allowed"
          :disabled="!!timeError || !meetupTimeWindow || !meetupDate || !meetupAddressQuery || loading"
        >
          <p v-if="!loading">Confirm Purchase</p>
          <p v-else>Processing...</p>
        </UButton>
      </div>
    </template>
  </UModal>
</template>
