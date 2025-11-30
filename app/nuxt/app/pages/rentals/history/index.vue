<script setup lang="ts">
import auth from '~/middleware/auth';
import RentalsSection from '~/components/RentalsSection.vue';
import { ref, computed } from 'vue';

definePageMeta({
  middleware: auth,
});

const activeTab = ref<'lending' | 'renting'>('lending');
const route = useRoute();

const tab = route.query.activeTab;
if (tab && !Array.isArray(tab)) {
  if (tab === 'lending' || tab === 'renting') {
    activeTab.value = tab;
  }
}

navigateTo({ query: { activeTab: activeTab.value } }, { replace: true });

const tabs = [
  { id: 'lending', label: "Books I've Lent", icon: 'lucide:trending-up' },
  { id: 'renting', label: "Books I've Rented", icon: 'lucide:trending-down' },
] as const;

const headerText = computed(() => {
  return activeTab.value === 'lending' ? 'Lend History' : 'Rent History';
});

watch(activeTab, (val) => {
  const url = new URL(window.location.href);
  url.searchParams.set('activeTab', val);
  window.history.replaceState({}, '', url.toString());
});
</script>

<template>
  <div class="flex flex-col min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mb-6 flex justify-between items-start">
      <div class="text-base">
        <h1 class="font-bold text-3xl flex items-center gap-2 mb-1">
          <Icon name="fluent:calendar-24-regular" class="w-8 h-8 text-orange-500" />
          Rental History
        </h1>
        <p class="text-muted">View lent and rent history</p>
      </div>
    </div>

    <div class="w-full bg-background">
      <div class="mx-auto">
        <div class="grid grid-cols-2 gap-3 mb-6">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="[
              'px-4 py-3 rounded-lg font-medium transition-all text-center cursor-pointer',
              activeTab === tab.id
                ? 'bg-accent text-white'
                : 'bg-surface text-foreground hover:bg-surface-hover',
            ]"
            @click="activeTab = tab.id"
          >
            <div class="flex items-center justify-center gap-1">
              <Icon :name="tab.icon" />
              <span class="text-sm leading-tight">{{ tab.label }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold text-foreground">{{ headerText }}</h2>
      <NuxtLink
        :to="{ path: '/rentals', query: { activeTab } }"
        class="text-foreground font-medium bg-default hover:bg-default active:bg-default flex items-center gap-1 cursor-pointer"
      >
        Transactions
        <Icon name="lucide:move-right" class="w-6 h-6 text-foreground" />
      </NuxtLink>
    </div>

    <!-- Pass activeTab to RentalsSection as prop -->
    <RentalsSection :active-tab="activeTab" />
  </div>
</template>
