<script setup lang="ts">
import { dateConverter, getDateDifference } from '#imports';

const props = defineProps<{
  isOpenNotificationModal: boolean;
  header: string | undefined;
  message: string | undefined;
  createdAt: string | undefined;
}>();

const emit = defineEmits<{
  (e: 'update:openNotificationModal', value: boolean): void;
}>();

const isOpenNotificationModal = computed({
  get: () => props.isOpenNotificationModal,
  set: (val: boolean) => {
    emit('update:openNotificationModal', val);
  },
});
</script>

<template>
  <UModal v-model:open="isOpenNotificationModal" :ui="{ content: 'max-w-2xl' }">
    <template #header>
      <h2 class="w-full font-bold text-2xl">{{ props.header }}</h2>
    </template>

    <template #body>
      <p class="text-justify">{{ props.message }}</p>
    </template>

    <template #footer>
      <p class="font-bold text-sm">
        {{ dateConverter(props.createdAt as string, 'long') }} ({{
          getDateDifference(props.createdAt as string)
        }})
      </p>
    </template>
  </UModal>
</template>
