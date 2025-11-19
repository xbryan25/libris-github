<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div class="flex flex-col w-full h-[88vh] pt-10 px-20 gap-5">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <Icon name="material-symbols:notifications-rounded" class="w-8 h-8 text-base" />
        <h1 class="font-bold text-3xl">Notifications</h1>
      </div>

      <p class="text-muted">Check your latest notifications and important actions.</p>
    </div>

    <NotificationsTable />
  </div>
</template>
