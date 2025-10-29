<script setup lang="ts">
import guest from '~/middleware/guest';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});
</script>

<template>
  <UApp>
    <div class="bg-gradient-to-b from-[#d7fff0] to-white min-h-screen w-full">
      <div class="absolute top-5 left-0 w-full flex justify-between items-center px-5">
        <div class="flex items-center space-x-3">
          <Icon name="icons:logo" class="w-12 h-12" />
          <h1 class="text-4xl font-bold text-[#000000]">Libris</h1>
        </div>

        <div class="flex items-center space-x-6">
          <NuxtLink
            to="/login"
            class="px-4 py-2 rounded-lg font-semibold text-xl text-gray-800 hover:bg-[#8CFFB6] transition-colors"
          >
            Sign-in
          </NuxtLink>
          <h1 class="text-xl font-semibold">Contact us</h1>
        </div>
      </div>

      <div class="absolute top-[22%] left-1/2 -translate-x-1/2 text-center">
        <h1 class="text-8xl font-extrabold text-[#111] tracking-tight">Create Your Own Library</h1>
        <h3 class="mt-4 text-2xl text-[#333] font-medium">
          Discover, rent, or share books near you
        </h3>
        <NuxtLink to="/signup">
          <UButton size="xl" class="mt-7 px-6 py-3 text-lg">Get Started</UButton>
        </NuxtLink>
      </div>

      <section class="absolute top-[58%] left-1/2 -translate-x-1/2 w-full max-w-6xl px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-14 text-center">
          <div>
            <Icon name="icons:profilecard" class="w-44 h-44 mx-auto mb-6" />
            <h3 class="text-3xl font-semibold text-[#111]">Build Your Profile</h3>
            <p class="mt-3 text-[#555] text-lg">Create a profile and organize your own library</p>
          </div>

          <div>
            <Icon name="icons:books" class="w-44 h-44 mx-auto mb-6" />
            <h3 class="text-3xl font-semibold text-[#111]">Explore Libraries</h3>
            <p class="mt-3 text-[#555] text-lg">Browse books from other users</p>
          </div>

          <div>
            <Icon name="icons:exchange" class="w-44 h-44 mx-auto mb-6" />
            <h3 class="text-3xl font-semibold text-[#111]">Share and Exchange</h3>
            <p class="mt-3 text-[#555] text-lg">Rent, lend, or sell books to fellow readers</p>
          </div>
        </div>
      </section>
    </div>
  </UApp>
</template>
