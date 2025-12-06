<script setup lang="ts">
import { useAuthStore } from './stores/useAuthStore';

useHead({
  title: 'Libris',
  meta: [{ name: 'description', content: 'Libris - a book rent-buy platform' }],
  link: [{ rel: 'icon', type: 'image/png', href: '/favicon.svg' }],
});

const toaster = { position: 'top-right' } as const;

const auth = useAuthStore();

watch(
  () => auth.userId,
  (userId, oldUserId) => {
    // Ignore the very first run if both undefined/null
    if (!userId && !oldUserId) return;

    if (oldUserId && !userId) {
      // User logged out
      useSocketLogout(oldUserId);
    }

    if (userId && userId !== oldUserId) {
      // User logged in or switched
      useSocket(userId);
    }
  },
);
</script>

<template>
  <UApp :toaster="toaster">
    <NuxtLayout />
  </UApp>
</template>

<style global>
/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Scrollbar customization for WebKit browsers (Chrome, Edge, Safari) */
::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1; /* track color */
  border-radius: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: #48bb78;
  border-radius: 6px;
  border: 3px solid #f1f1f1;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #38a169;
}

* {
  scrollbar-width: thin;
  scrollbar-color: #48bb78 #f1f1f1;
}
</style>
