<script setup lang="ts">
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
            <div class="flex items-center gap-1">
              <span>{{ props.bookTitle }}</span>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm text-base">
            <span>Author:</span>
            <div class="flex items-center gap-1">
              <span>{{ props.bookAuthor }}</span>
            </div>
          </div>
          
          <USeparator orientation="horizontal" class="my-2 bg-slate-400" />

          <div class="flex items-center justify-between font-semibold text-base">
            <span>Total Cost:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>{{ props.purchasePrice }}</span>
            </div>
          </div>

          <div class="flex items-center justify-between font-semibold text-base">
            <span>Your Balance:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>{{ props.currentWalletBalance }}</span>
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <UButton class="bg-slate-300 hover:bg-slate-400 text-black dark:bg-slate-400 dark:hover:bg-slate-500 px-4 py-2 rounded">
          <p>Cancel</p> 
          </UButton>
          <UButton class="bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-4 py-2 rounded">
          <p>Confirm Purchase</p> 
          </UButton>
        </div>
  </template>
  </UModal>
</template>
