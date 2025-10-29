<script setup lang="ts">
import guest from '~/middleware/guest';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});
</script>

<template>
  <h1>Sign Up Page</h1>
</template>
