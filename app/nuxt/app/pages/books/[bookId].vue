<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});

const route = useRoute();
const bookId = route.params.bookId as string;

// Use bookId for query book details in db
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <h1 class="text-5xl font-bold text-primary">{{ bookId }}</h1>
  </div>
</template>
