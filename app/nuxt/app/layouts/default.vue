<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuthStore';
import type { TabsItem } from '@nuxt/ui';

const tabItems = [
  {
    label: 'Unread',
    icon: 'i-lucide-user',
    slot: 'unread',
  },
  {
    label: 'Read',
    icon: 'i-lucide-lock',
    slot: 'read',
  },
];
const route = useRoute();

const auth = useAuthStore();

const { paymentSuccess } = useSocket(auth.userId as string);

const currentWalletBalance = ref(0);
const isFetching = ref(true);

const isOpenNotificationPopover = ref(false);

const isActive = (path: string) => {
  if (route.path === path) return true;

  if (route.path.startsWith('/books/') && route.query.from) {
    if (path === '/browse' && route.query.from === 'browse') return true;
  }

  return false;
};

watch(
  () => paymentSuccess.value,
  (amount) => {
    if (amount) {
      currentWalletBalance.value = currentWalletBalance.value + amount;
    }
  },
);

onMounted(async () => {
  isFetching.value = true;

  const data = await useCurrentWalletBalance();
  currentWalletBalance.value = data.currentWalletBalance ?? 0;

  isFetching.value = false;
});
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
              isActive('/dashboard')
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base',
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
              isActive('/browse')
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base',
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
              isActive('/library')
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base',
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
              isActive('/rentals')
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base',
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
              isActive('/purchases')
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base',
            ]"
          >
            <Icon
              name="material-symbols:shopping-cart-outline-rounded"
              class="w-5 h-5 flex-shrink-0"
            />
            <span>Purchases</span>
          </NuxtLink>

          <!-- Profile -->
          <NuxtLink
            to="/users/me"
            :class="[
              'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors',
              isActive('/users/me')
                ? 'bg-accent text-white'
                : 'hover:bg-surface-hover hover:text-accent text-base',
            ]"
          >
            <Icon name="lucide:circle-user" class="w-5 h-5 flex-shrink-0" />
            <span>Profile</span>
          </NuxtLink>

          <!-- Readits Display -->
          <NuxtLink
            class="flex items-center rounded-md px-3 py-2 gap-1.5 hover:bg-surface-hover hover:text-accent text-base"
            to="/buy-readits"
          >
            <Icon name="fluent:book-coins-20-regular" class="w-6 h-6 text-accent" />

            <span v-if="isFetching" class="text-xl font-semibold text-accent">-</span>
            <span v-else class="text-xl font-semibold text-accent">{{ currentWalletBalance }}</span>
          </NuxtLink>

          <!-- Notifications -->

          <UPopover v-model:open="isOpenNotificationPopover" arrow>
            <UChip text="9" size="3xl">
              <UButton
                icon="mdi:bell-outline"
                class="flex items-center rounded-md p-2 bg-surface hover:bg-surface-hover hover:text-accent text-base cursor-pointer transition-colors"
              />
            </UChip>

            <template #content>
              <div class="w-75 h-80 p-2 flex flex-col gap-1">
                <h1 class="font-bold text-xl">Notifications</h1>

                <UTabs
                  color="neutral"
                  :items="tabItems"
                  class="w-full"
                  :ui="{
                    trigger: 'cursor-pointer',
                  }"
                >
                  <template #unread>
                    <div class="flex flex-col gap-2">
                      <div class="cursor-pointer border-2 border-surface p-2 rounded-md">
                        <h2 class="font-semibold text-sm">Request Approved!</h2>
                        <p class="text-xs w-full truncate">
                          The request to rent 'The Passion Within' has been approved.
                        </p>
                      </div>

                      <div class="cursor-pointer border-2 border-surface p-2 rounded-md">
                        <h2 class="font-semibold text-sm">Request Approved!</h2>
                        <p class="text-xs w-full truncate">
                          The request to rent 'The Passion Within' has been approved.
                        </p>
                      </div>

                      <div class="cursor-pointer border-2 border-surface p-2 rounded-md">
                        <h2 class="font-semibold text-sm">Request Approved!</h2>
                        <p class="text-xs w-full truncate">
                          The request to rent 'The Passion Within' has been approved.
                        </p>
                      </div>

                      <UButton color="neutral" class="justify-center cursor-pointer"
                        >See more (99)</UButton
                      >
                    </div>
                  </template>

                  <template #read>
                    <div class="flex flex-col gap-2">
                      <div class="cursor-pointer border-2 border-surface p-2 rounded-md">
                        <h2 class="font-semibold text-sm">Request Approved!</h2>
                        <p class="text-xs w-full truncate">
                          The request to rent 'The Passion Within' has been approved.
                        </p>
                      </div>

                      <div class="cursor-pointer border-2 border-surface p-2 rounded-md">
                        <h2 class="font-semibold text-sm">Request Approved!</h2>
                        <p class="text-xs w-full truncate">
                          The request to rent 'The Passion Within' has been approved.
                        </p>
                      </div>

                      <div class="cursor-pointer border-2 border-surface p-2 rounded-md">
                        <h2 class="font-semibold text-sm">Request Approved!</h2>
                        <p class="text-xs w-full truncate">
                          The request to rent 'The Passion Within' has been approved.
                        </p>
                      </div>

                      <UButton color="neutral" class="justify-center cursor-pointer"
                        >See more</UButton
                      >
                    </div>
                  </template>
                </UTabs>
              </div>
            </template>
          </UPopover>

          <!-- <button
            class="flex items-center rounded-md p-2 hover:bg-surface-hover hover:text-accent text-base cursor-pointer transition-colors"
          >
            <Icon name="mdi:bell-outline" class="w-5 h-5" />
          </button> -->

          <!-- Color Mode Toggle -->
          <ColorModeButton class="hover:text-accent hover:bg-surface-hover transition-colors" />

          <LogoutButton />
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 justify-center items-center bg-background">
      <NuxtPage />
    </main>
  </div>
</template>
