<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full">
    <BookList />
  </div>
</template>
