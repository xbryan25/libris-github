<script setup lang="ts">
const props = defineProps<{
  isOpenNotificationActionsModal: boolean;
  selectedNotificationAction: string;
  selectedRows: Set<string>;
  determineIsReadChange: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:openNotificationActionsModal', value: boolean): void;
  (e: 'onSuccessfulUpdate' | 'onSuccessfulDelete'): void;
}>();

const isLoading = ref(false);

const toast = useToast();

const isOpenNotificationActionsModal = computed({
  get: () => props.isOpenNotificationActionsModal,
  set: (val: boolean) => {
    emit('update:openNotificationActionsModal', val);
  },
});

const markSelectedNotificationsAsRead = async (): Promise<void> => {
  isLoading.value = true;

  await useChangeNotificationsReadStatus(props.selectedRows, props.determineIsReadChange);

  toast.add({
    description: `${props.selectedRows.size} notification${props.selectedRows.size > 1 ? 's' : ''} marked as ${props.determineIsReadChange ? 'unread' : 'read'}.`,
    color: 'success',
  });

  emit('onSuccessfulUpdate');
};

const deleteSelectedNotifications = async () => {
  isLoading.value = true;

  await useDeleteNotifications(props.selectedRows);

  toast.add({
    description: `${props.selectedRows.size} notification${props.selectedRows.size > 1 ? 's' : ''} deleted.`,
    color: 'success',
  });

  emit('onSuccessfulDelete');
};

watch(
  () => props.isOpenNotificationActionsModal,
  async (newValue) => {
    if (!newValue) {
      setTimeout(() => {
        isLoading.value = false;
      }, 500);
    }
  },
);
</script>

<template>
  <UModal v-model:open="isOpenNotificationActionsModal">
    <template #header>
      <h2 v-if="props.selectedNotificationAction == 'delete'" class="w-full font-bold text-2xl">
        Delete notifications
      </h2>
      <h2 v-else class="w-full font-bold text-2xl">
        Mark notifications as
        {{ props.selectedNotificationAction == 'markRead' ? 'read' : 'unread' }}
      </h2>
    </template>

    <template #body>
      <div class="flex flex-col justify-center min-h-15">
        <p
          v-if="props.selectedNotificationAction == 'delete'"
          class="font-bold text-lg text-center"
        >
          Confirm deletion of {{ props.selectedRows.size }}
          {{ props.selectedRows.size > 1 ? 'notifications' : 'notification' }}?
        </p>

        <p v-else class="font-bold text-lg text-center">
          Confirm marking
          {{
            props.selectedRows.size > 1
              ? `${props.selectedRows.size} notifications`
              : '1 notification'
          }}
          as
          {{ props.selectedNotificationAction == 'markRead' ? 'read' : 'unread' }}?
        </p>

        <div class="flex justify-center gap-2 w-full pt-5">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpenNotificationActionsModal = false"
            >Cancel</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            class="cursor-pointer"
            :loading="isLoading"
            :disabled="isLoading"
            @click="
              async () => {
                if (props.selectedNotificationAction == 'delete') {
                  await deleteSelectedNotifications();
                } else {
                  await markSelectedNotificationsAsRead();
                }

                isOpenNotificationActionsModal = false;
              }
            "
            >Proceed</UButton
          >
        </div>
      </div>
    </template>
  </UModal>
</template>
