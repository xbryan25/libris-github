<script setup lang="ts">
import guest from '~/middleware/guest';

definePageMeta({
  layout: 'unauthenticated',
  middleware: guest,
});
</script>

<template>
  <UApp>
    <div
      class="bg-gradient-to-b from-[#d7fff0] to-white min-h-screen w-full flex flex-col"
    >
      <div class="top-5 left-0 w-full flex justify-between items-center px-5 pt-5">
        <div class="flex items-center space-x-3">
          <Icon name="icons:logo" class="w-12 h-12 text-primary" />
          <h1 class="text-4xl font-bold text-[#000000]">Libris</h1>
        </div>

        <div class="flex items-center space-x-6">
          <NuxtLink
            to="/login"
            class="px-4 py-2 rounded-lg font-semibold text-xl text-gray-800 hover:bg-[#8CFFB6] transition-colors"
          >
            Sign-in
          </NuxtLink>
          <NuxtLink to="#contact" class="text-xl font-semibold text-gray-700 hover:text-black">Contact us</NuxtLink>
        </div>
      </div>

      <div class="flex flex-col justify-center text-center py-24 sm:py-32">
        <h1 class="text-6xl sm:text-8xl font-extrabold text-[#111] tracking-tight">Create Your Own Library</h1>
        <h3 class="mt-4 text-xl sm:text-2xl text-[#333] font-medium">
          Discover, rent, or share books near you
        </h3>
        <NuxtLink to="/signup" class="mx-auto">
          <UButton size="xl" class="mt-7 px-6 py-3 text-lg cursor-pointer">Get Started</UButton>
        </NuxtLink>
      </div>

      <section class="flex justify-center w-full px-8 pb-24 sm:pb-32">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-14 text-center">
          
          <NuxtLink to="#build" class="block p-6 rounded-xl hover:bg-white/60 transition-all transform hover:-translate-y-1">
            <Icon name="icons:profilecard" class="w-32 h-32 sm:w-44 sm:h-44 mx-auto mb-6 text-primary" />
            <h3 class="text-3xl font-semibold text-[#111]">Build Your Profile</h3>
            <p class="mt-3 text-[#555] text-lg">Create a profile and organize your own library</p>
          </NuxtLink>

          <NuxtLink to="#explore" class="block p-6 rounded-xl hover:bg-white/60 transition-all transform hover:-translate-y-1">
            <Icon name="icons:books" class="w-32 h-32 sm:w-44 sm:h-44 mx-auto mb-6 text-primary" />
            <h3 class="text-3xl font-semibold text-[#111]">Explore Libraries</h3>
            <p class="mt-3 text-[#555] text-lg">Browse books from other users</p>
          </NuxtLink>

          <NuxtLink to="#share" class="block p-6 rounded-xl hover:bg-white/60 transition-all transform hover:-translate-y-1">
            <Icon name="icons:exchange" class="w-32 h-32 sm:w-44 sm:h-44 mx-auto mb-6 text-primary" />
            <h3 class="text-3xl font-semibold text-[#111]">Share and Exchange</h3>
            <p class="mt-3 text-[#555] text-lg">Rent, lend, or sell books to fellow readers</p>
          </NuxtLink>

        </div>
      </section>


      <div id="build" class="py-16 sm:py-24 scroll-mt-16">
        <UContainer>
          <h2 class="text-3xl font-bold tracking-tight text-center sm:text-4xl text-[#111]">
            Build Your Profile in Minutes
          </h2>
          <p class="mt-4 text-lg text-gray-600 text-center">
            Your personal library, beautifully organized and ready to share.
          </p>
          
          <UCard class="mt-12">
            <template #header>
              <h3 class="text-xl font-semibold">Your Profile Details</h3>
            </template>

          </UCard>
        </UContainer>
      </div>

      <div id="explore" class="py-16 sm:py-24 bg-gray-50 dark:bg-gray-900/50 scroll-mt-16">
        <UContainer>
          <h2 class="text-3xl font-bold tracking-tight text-center sm:text-4xl text-[#111]">
            Discover a World of Books Nearby
          </h2>
          <p class="mt-4 text-lg text-gray-600 text-center">
            Find exactly what you're looking for, right in your neighborhood.
          </p>
          
          <UCard class="mt-12">
            <template #header>
              <h3 class="text-xl font-semibold">Explore Feature Details</h3>
            </template>

          </UCard>
        </UContainer>
      </div>

      <div id="share" class="py-16 sm:py-24 scroll-mt-16">
        <UContainer>
          <h2 class="text-3xl font-bold tracking-tight text-center sm:text-4xl text-[#111]">
            Connect, Share, and Read More
          </h2>
          <p class="mt-4 text-lg text-gray-600 text-center">
            A safe and easy way to lend, rent, or sell your books.
          </p>
          
          <UCard class="mt-12">
            <template #header>
              <h3 class="text-xl font-semibold">Sharing & Exchange Details</h3>
            </template>

          </UCard>
        </UContainer>
      </div>

      <footer id="contact" class="py-8 border-t border-gray-200 dark:border-gray-800 mt-16">
        <UContainer>
            <p class="text-sm text-gray-500 text-right mt-4 sm:mt-0">
              &copy; {{ new Date().getFullYear() }} Libris. All rights reserved.
            </p>
        </UContainer>
      </footer>

    </div>
  </UApp>
</template>
