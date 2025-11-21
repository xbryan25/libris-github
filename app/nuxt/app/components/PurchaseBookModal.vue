<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAddressAutocomplete } from '~/composables/useAddressAutocomplete'

const LOCATIONIQ_API_KEY = import.meta.env.VITE_LOCATIONIQ_API_KEY

const meetupAddress = ref('')
const { 
  addressQuery: meetupAddressQuery, 
  suggestions: meetupSuggestions, 
  fetchSuggestions: fetchMeetupSuggestions, 
  selectSuggestion: selectMeetupSuggestion 
} = useAddressAutocomplete(LOCATIONIQ_API_KEY)

const meetupDate = ref<string | null>(null)

const props = defineProps<{
  isOpenPurchaseBookModal: boolean
  bookTitle?: string
  bookAuthor?: string
  purchasePrice?: number
  currentWalletBalance?: number
}>()

const emit = defineEmits<{
  (e: 'update:openPurchaseBookModal', value: boolean): void
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
  selectMeetupSuggestion(item, meetupAddress)
  meetupAddressQuery.value = item.display_name
  meetupAddress.value = item.display_name
  meetupSuggestions.value = []
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

  <!-- Meetup Inputs Outside Gray Box -->
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

  <!-- Buttons -->
  <div class="flex justify-end gap-3 mt-6">
    <UButton 
      @click="isOpenPurchaseBookModal = false" 
      class="bg-slate-300 hover:bg-slate-400 text-black dark:bg-slate-400 dark:hover:bg-slate-500 px-4 py-2 rounded"
    >
      <p>Cancel</p> 
    </UButton>
    <UButton 
      class="bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-4 py-2 rounded"
    >
      <p>Confirm Purchase</p> 
    </UButton>
  </div>
</template>
  </UModal>
</template>
