<script setup lang="ts">
const props = defineProps<{
  isOpenRentBookModal: boolean
}>()

const emit = defineEmits<{
  (e: 'update:openRentBookModal', value: boolean): void
}>()

const isOpenRentBookModal = computed({
  get: () => props.isOpenRentBookModal,
  set: (val: boolean) => emit('update:openRentBookModal', val)
})
</script>

<template>
  <UModal v-model:open="isOpenRentBookModal" :ui="{ content: 'max-w-lg' }" :dismissible="true">
    <template #header>
      <h2 class="text-2xl font-semibold">Rent This Book</h2>
    </template>

    <template #body>
      <div class="p-4 space-y-4">
        <p class="text-muted">Rental request form goes here.</p>
      </div>
    </template>
  </UModal>
</template>
