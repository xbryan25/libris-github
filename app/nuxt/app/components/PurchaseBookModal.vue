<script setup lang="ts">
const props = defineProps<{
  isOpenPurchaseBookModal: boolean
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
      <h2 class="text-2xl font-semibold">Purchase This Book</h2>
    </template>

    <template #body>
      <div class="p-4 space-y-4">
        <p class="text-muted">Purchase request form goes here.</p>
      </div>
    </template>
  </UModal>
</template>
