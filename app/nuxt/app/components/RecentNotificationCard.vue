<script setup lang="ts">
import type { Notification } from '~/types';

const props = defineProps<{
  notificationDetails: Notification;
}>();
</script>

<template>
  <NuxtLink
    :to="`notifications/${notificationDetails.notificationId}`"
    class="cursor-pointer border-2 border-surface p-2 rounded-md hover:bg-surface-hover"
  >
    <h2 class="font-semibold text-sm">{{ props.notificationDetails.header }}</h2>
    <p class="text-xs w-full truncate">
      {{ props.notificationDetails.message }}
    </p>
  </NuxtLink>
</template>
