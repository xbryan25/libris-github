<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <h1 class="text-5xl font-bold text-primary">Purchases Page</h1>
  </div>
</template>
