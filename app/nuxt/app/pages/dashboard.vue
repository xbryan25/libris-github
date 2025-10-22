<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div class="flex items-center justify-center w-full">
    <h1 class="text-5xl font-bold text-primary">Dashboard Page</h1>
  </div>
</template>
