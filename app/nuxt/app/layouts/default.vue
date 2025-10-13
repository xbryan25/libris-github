<script setup lang="ts">
  const route = useRoute()
</script>

<template>
  <div class="min-h-screen w-full flex flex-col bg-background text-base">
    <!-- Navbar -->
    <nav class="w-full border-b border-base bg-surface">
      <div class="w-full flex items-center justify-between px-6 py-4">
        <!-- Logo -->
        <div class="flex items-center gap-2 ml-8">
          <Icon name="icons:logo" class="w-9 h-9 text-accent" />
          <h1 class="text-2xl font-semibold">Libris</h1>
        </div>

        <div class="flex items-center gap-1 mr-8">
          <!-- Dashboard -->
          <NuxtLink
            to="/dashboard"
            :class="[ 
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === '/dashboard'
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base'
            ]"
          >
            <Icon name="ri:dashboard-line" class="w-5 h-5 flex-shrink-0" />
            <span>Dashboard</span>
          </NuxtLink>

          <!-- Browse -->
          <NuxtLink
            to="/browse"
            :class="[ 
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === '/browse'
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base'
            ]"
          >
            <Icon name="ph:magnifying-glass-bold" class="w-5 h-5" />
            <span>Browse</span>
          </NuxtLink>

          <!-- My Library -->
          <NuxtLink
            to="/library"
            :class="[ 
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === '/library'
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base'
            ]"
          >
            <Icon name="lucide:book-open" class="w-5 h-5 flex-shrink-0" />
            <span>My Library</span>
          </NuxtLink>

          <!-- Rentals -->
          <NuxtLink
            to="/rentals"
            :class="[ 
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === '/rentals'
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base'
            ]"
          >
            <Icon name="ci-calendar" class="w-5 h-5 flex-shrink-0" />
            <span>Rentals</span>
          </NuxtLink>

          <!-- Purchases -->
          <NuxtLink
            to="/purchases"
            :class="[ 
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === '/purchases'
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base'
            ]"
          >
            <Icon name="material-symbols:shopping-cart-outline-rounded" class="w-5 h-5 flex-shrink-0" />
            <span>Purchases</span>
          </NuxtLink>

          <!-- Profile -->
          <NuxtLink
            to="/profile"
            :class="[ 
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === '/profile'
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base'
            ]"
          >
            <Icon name="lucide:circle-user" class="w-5 h-5 flex-shrink-0" />
            <span>Profile</span>
          </NuxtLink>

          <!-- Readits Display -->
          <div class="flex items-center rounded-md px-3 py-2 gap-1.5">
            <Icon name="fluent:book-coins-20-regular" class="w-6 h-6 text-accent" />
            <span class="text-xl font-semibold text-accent">75</span>
          </div>

          <!-- Notifications -->
          <button class="flex items-center rounded-md p-2 hover:bg-surface-hover hover:text-accent text-base transition-colors">
            <Icon name="mdi:bell-outline" class="w-5 h-5" />
          </button>

          <!-- Color Mode Toggle -->
          <ColorModeButton class="hover:text-accent hover:bg-surface-hover transition-colors"/>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 flex justify-center items-center bg-background">
      <NuxtPage />
    </main>
  </div>
</template>
