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
const rentd = ref(['1 days', '3 days', '5 days', '7 days', '10 days', '14 days'])
</script>

<template>
  <UModal v-model:open="isOpenRentBookModal" :ui="{ content: 'max-w-lg' }" :dismissible="true">
    <template #header>
      <h2 class="text-2xl font-semibold">Rent "The Passion Within"</h2>
    </template>

    <template #body>
        <div class="p-4 bg-[#F4F4F5] space-y-3">
          <p class="font-semibold text-black">Rental Details</p>

          <div class="flex items-center justify-between text-sm text-gray-600">
            <span>Daily Rate:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>5/day</span>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm text-gray-600">
            <span>Security Deposit:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>15</span>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm text-gray-600">
            <span>Rental Period:</span>
            <span>14</span>
          </div>

          <USeparator orientation="horizontal" class="my-2" />

          <div class="flex items-center justify-between font-semibold text-black">
            <span>Total Cost:</span>
            <div class="flex items-center gap-1">
              <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent"/>
              <span>85</span>
            </div>
          </div>
        </div>

        <p class="font-semibold text-black mt-4">Rental Duration</p>
        <USelect :items="rentd" class="w-full mt-2" />
      <p class="font-semibold text-black">Meetup Location</p>
  </template>
  </UModal>
</template>
