<script setup lang="ts">
import type { Notification } from '~/types';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
}>();

const clickedRow = ref<Notification | null>(null);
const isOpenNotificationModal = ref(false);

const recentNotifications = ref<Notification[]>([]);
const isFetching = ref(false);
const maxNumOfRecentNotfications: number = 4;

const unreadNotificationsCount: Ref<number> = ref<number>(0);

const isOpen = computed({
  get: () => props.isOpen,
  set: (val: boolean) => {
    emit('update:isOpen', val);
  },
});

const chipText = computed(() => {
  const count = unreadNotificationsCount.value;
  return count > 99 ? '99+' : count.toString();
});

onMounted(async () => {
  isFetching.value = true;

  const options = {
    rowsPerPage: maxNumOfRecentNotfications,
    pageNumber: 1,
    readStatus: 'show only unread',
    order: 'show newest first',
  };

  recentNotifications.value = await useNotifications(options);

  const { totalCount }: { totalCount: number } =
    await useNotificationsTotalCount('show only unread');

  unreadNotificationsCount.value = totalCount;

  console.log(recentNotifications.value);

  isFetching.value = false;
});
</script>

<template>
  <UPopover v-model:open="isOpen" arrow>
    <div>
      <UChip
        v-if="unreadNotificationsCount > 0"
        :text="chipText"
        size="3xl"
        :ui="{ base: 'py-2 px-1' }"
      >
        <UButton
          icon="mdi:bell-outline"
          class="flex items-center rounded-md p-2 bg-surface hover:bg-surface-hover hover:text-accent text-base cursor-pointer transition-colors"
        />
      </UChip>

      <UButton
        v-else
        icon="mdi:bell-outline"
        class="flex items-center rounded-md p-2 bg-surface hover:bg-surface-hover hover:text-accent text-base cursor-pointer transition-colors"
      />
    </div>

    <template #content>
      <div class="w-75 h-85 p-2 flex flex-col gap-2">
        <h1 class="font-bold text-xl">Unread Notifications</h1>

        <div v-if="recentNotifications.length > 0" class="flex-1 flex flex-col gap-2">
          <RecentNotificationCard
            v-for="notification in recentNotifications"
            :key="notification.notificationId"
            :notification-details="notification"
            @click="
              clickedRow = notification;
              isOpenNotificationModal = true;
            "
          />
        </div>

        <div v-else class="flex-1 flex justify-center items-center">
          <p class="text-sm">Notifications will show up here...</p>
        </div>

        <NuxtLink to="/notifications" class="w-full">
          <UButton color="neutral" class="justify-center cursor-pointer w-full"
            >See more...</UButton
          >
        </NuxtLink>
      </div>

      <NotificationDetailsModal
        :is-open-notification-modal="isOpenNotificationModal"
        :header="clickedRow?.header"
        :message="clickedRow?.message"
        :created-at="clickedRow?.createdAt"
        @update:open-notification-modal="
          (newIsOpenNotificationModal: boolean) =>
            (isOpenNotificationModal = newIsOpenNotificationModal)
        "
      />
    </template>
  </UPopover>
</template>
