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
      class="bg-gradient-to-b from-[#e2fbce] via-[#e3ef26] to-[#07653] min-h-screen w-full flex flex-col"
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

      <div id="build" class="py-24 sm:py-32 scroll-mt-16">
        <UContainer>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            

            <div class="lg:order-1 text-center lg:text-left">
              <h2 class="text-4xl font-bold tracking-tight sm:text-5xl text-[#111]">
                Build Your Profile and Create Your Library
              </h2>
              <p class="mt-6 text-xl text-gray-600">
                Create your personal library. Effortlessly catalog your collection and let others discover your books.
              </p>
            </div>
            

            <div class="lg:order-2 flex justify-center items-center">
                <NuxtImg src="/images/BuildImage.png" class="w-full h-full object-cover" alt="Build image" />
            </div>
          </div>
        </UContainer>
      </div>

      <div id="explore" class="py-24 sm:py-32  scroll-mt-16">
        <UContainer>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            

            <div class="lg:order-1 flex justify-center items-center">
              <NuxtImg
                src="/images/BrowseImage.png"
                class="w-full h-full object-cover -translate-x-4 lg:-translate-x-20"
                alt="Browse image"
              />
            </div>


            <div class="lg:order-2 text-center lg:text-left">
              <h2 class="text-4xl font-bold tracking-tight sm:text-5xl text-[#111]">
                Browse Books Near You
              </h2>
              <p class="mt-6 text-xl text-gray-600">
                Find exactly what you're looking for, right in your neighborhood. Browse books from other users, filter by genre, author, title, price, distance to find your next great read.
              </p>
            </div>
          </div>
        </UContainer>
      </div>

      <div id="share" class="py-24 sm:py-32 scroll-mt-16">
        <UContainer>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            

            <div class="lg:order-1 text-center lg:text-left">
              <h2 class="text-4xl font-bold tracking-tight sm:text-5xl text-[#111]">
                Connect, Share, and Read More
              </h2>
              <p class="mt-6 text-xl text-gray-600">
                A safe and easy way to lend, rent, or sell your books. Communicate with user, arrange a public meetup, and rate other users.
              </p>
              <ul class="mt-8 space-y-4 text-xl text-gray-700 text-center lg:text-left">
                <li class="flex items-center justify-center lg:justify-start">
                  <Icon name="i-heroicons-check-circle-solid" class="w-7 h-7 text-green-500 mr-3 flex-shrink-0" />
                  <span>Lend/Sell your books</span>
                </li>
                <li class="flex items-center justify-center lg:justify-start">
                  <Icon name="i-heroicons-check-circle-solid" class="w-7 h-7 text-green-500 mr-3 flex-shrink-0" />
                  <span>Borrow/Purchase books from others</span>
                </li>
                <li class="flex items-center justify-center lg:justify-start">
                  <Icon name="i-heroicons-check-circle-solid" class="w-7 h-7 text-green-500 mr-3 flex-shrink-0" />
                  <span>Rate other users after each transaction</span>
                </li>
              </ul>
            </div>
            

            <div class="lg:order-2 flex justify-center items-center">
                <NuxtImg src="/images/ShareImage.png" class="w-full h-full object-cover" alt="Build image" />
            </div>
          </div>
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