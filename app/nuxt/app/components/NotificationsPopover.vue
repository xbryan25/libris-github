<script setup lang="ts">
const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
}>();

const tabItems = [
  {
    label: 'Unread',
    slot: 'unread',
  },
  {
    label: 'Read',
    slot: 'read',
  },
];

const isOpen = computed({
  get: () => props.isOpen,
  set: (val: boolean) => {
    emit('update:isOpen', val);
  },
});
</script>

<template>
  <UPopover v-model:open="isOpen" arrow>
    <UChip text="9" size="3xl">
      <UButton
        icon="mdi:bell-outline"
        class="flex items-center rounded-md p-2 bg-surface hover:bg-surface-hover hover:text-accent text-base cursor-pointer transition-colors"
      />
    </UChip>

    <template #content>
      <div class="w-75 h-85 p-2 flex flex-col gap-2">
        <h1 class="font-bold text-xl">Latest Notifications</h1>

        <div class="flex flex-col gap-2">
          <div class="cursor-pointer border-2 border-surface p-2 rounded-md hover:bg-surface-hover">
            <h2 class="font-semibold text-sm">Request Approved!</h2>
            <p class="text-xs w-full truncate">
              The request to rent 'The Passion Within' has been approved.
            </p>
          </div>

          <div class="cursor-pointer border-2 border-surface p-2 rounded-md hover:bg-surface-hover">
            <h2 class="font-semibold text-sm">Request Approved!</h2>
            <p class="text-xs w-full truncate">
              The request to rent 'The Passion Within' has been approved.
            </p>
          </div>

          <div class="cursor-pointer border-2 border-surface p-2 rounded-md hover:bg-surface-hover">
            <h2 class="font-semibold text-sm">Request Approved!</h2>
            <p class="text-xs w-full truncate">
              The request to rent 'The Passion Within' has been approved.
            </p>
          </div>

          <div class="cursor-pointer border-2 border-surface p-2 rounded-md hover:bg-surface-hover">
            <h2 class="font-semibold text-sm">Request Approved!</h2>
            <p class="text-xs w-full truncate">
              The request to rent 'The Passion Within' has been approved.
            </p>
          </div>

          <NuxtLink to="/notifications" class="w-full">
            <UButton color="neutral" class="justify-center cursor-pointer w-full"
              >See more (99)</UButton
            >
          </NuxtLink>
        </div>
      </div>
    </template>
  </UPopover>
</template>
