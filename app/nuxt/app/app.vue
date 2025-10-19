<script setup lang="ts">
useHead({
  title: 'Libris',
  meta: [{ name: 'description', content: 'Libris - a book rent-buy platform' }],
  link: [{ rel: 'icon', type: 'image/png', href: '/favicon.svg' }],
});

const toaster = { position: 'top-right' } as const;
</script>

<template>
  <UApp :toaster="toaster">
    <NuxtLayout />
  </UApp>
</template>
