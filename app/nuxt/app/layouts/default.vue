<template>
  <div class="min-h-screen w-full flex flex-col">
    <!-- Navbar -->
    <nav class="w-full border-b border-slate-300">
      <div class="w-full flex items-center justify-between px-6 py-4">
        <!-- Logo -->
        <div class="flex items-center gap-2 ml-8">
          <Icon name="icons:logo" class="w-9 h-9" />
          <span class="text-2xl font-semibold">
            Libris
          </span>
        </div>

        <div class="flex items-center gap-1 mr-8">
          <!-- Navigation Links -->
          <NuxtLink to="/dashboard" class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition-colors">
            <Icon name="ri:dashboard-line" class="w-5 h-5 flex-shrink-0"/>
            <span class="text-sm font-medium text-slate-700 hover:text-slate-900">Dashboard</span>
          </NuxtLink>

          <NuxtLink to="/browse" class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition-colors">
            <Icon name="ph:magnifying-glass-bold" class="w-5 h-5"/>
            <span class="text-sm font-medium text-slate-700 hover:text-slate-900">Browse</span>
          </NuxtLink>

          <NuxtLink to="/library" class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition-colors">
            <Icon name="lucide:book-open" class="w-5 h-5 flex-shrink-0"/>
            <span class="text-sm font-medium text-slate-700 hover:text-slate-900">My Library</span>
          </NuxtLink>

          <NuxtLink to="/rentals" class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition-colors">
            <Icon name="ci-calendar" class="w-5 h-5 flex-shrink-0"/>
            <span class="text-sm font-medium text-slate-700 hover:text-slate-900">Rentals</span>
          </NuxtLink>

          <NuxtLink to="/purchases" class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition-colors">
            <Icon name="material-symbols:shopping-cart-outline-rounded" class="w-5 h-5 flex-shrink-0"/>
            <span class="text-sm font-medium text-slate-700 hover:text-slate-900">Purchases</span>
          </NuxtLink>

          <NuxtLink to="/profile" class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition-colors">
            <Icon name="lucide:circle-user" class="w-5 h-5 flex-shrink-0"/>
            <span class="text-sm font-medium text-slate-700 hover:text-slate-900">Profile</span>
          </NuxtLink>

          <!-- Readits Display -->
          <div class="flex items-center rounded-md px-3 py-2 gap-1.5">
            <Icon name="fluent:book-coins-20-regular" class="w-6 h-6 text-green-600"/>
            <span class="text-xl font-semibold text-green-600">75</span>
          </div>

          <!-- Notifications -->
          <button class="flex items-center rounded-md p-2 transition-colors">
            <Icon name="mdi:bell-outline" class="w-5 h-5"/>
          </button>
        </div>
      </div>
    </nav>
    <!-- Main Content -->
    <main class="flex-1 flex justify-center items-center">
      <NuxtPage />
    </main>
  </div>
</template>
