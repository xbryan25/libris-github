<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div
    class="flex flex-col items-center justify-center w-full min-h-screen pt-4 px-4 md:px-8 lg:px-15"
  >
    <BookList />
  </div>
</template>
