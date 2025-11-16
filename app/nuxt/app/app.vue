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
  background: #f1f1f1;   /* track color */
  border-radius: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: #48BB78; 
  border-radius: 6px;       
  border: 3px solid #f1f1f1; 
}

::-webkit-scrollbar-thumb:hover {
  background-color: #38a169; 
}

* {
  scrollbar-width: thin;          
  scrollbar-color: #48BB78 #f1f1f1; 
}
</style>