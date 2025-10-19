<script setup lang="ts">
import guest from '~/middleware/guest';

definePageMeta({
  middleware: guest,
});
</script>

<template>
  <h1>Sign In Page</h1>
</template>
