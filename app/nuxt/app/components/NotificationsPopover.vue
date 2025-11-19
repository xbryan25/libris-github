<script setup lang="ts">
import type { Notification } from '~/types';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
}>();

const recentNotifications = ref<Notification[]>([]);
const isFetching = ref(false);
const maxNumOfRecentNotfications: number = 4;

const isOpen = computed({
  get: () => props.isOpen,
  set: (val: boolean) => {
    emit('update:isOpen', val);
  },
});

onMounted(async () => {
  isFetching.value = true;

  recentNotifications.value = await useRecentNotifications(maxNumOfRecentNotfications);

  console.log(recentNotifications.value);

  isFetching.value = false;
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
        <h1 class="font-bold text-xl">Unread Notifications</h1>

        <div v-if="recentNotifications.length > 0" class="flex-1 flex flex-col gap-2">
          <RecentNotificationCard
            v-for="notification in recentNotifications"
            :key="notification.notificationId"
            :notification-details="notification"
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
    </template>
  </UPopover>
</template>
