<script setup lang="ts">
import auth from '~/middleware/auth';
import RentalsSection from '~/components/RentalsSection.vue';
import { ref, computed } from 'vue';

definePageMeta({
  middleware: auth,
});

const activeTab = ref<'lending' | 'renting'>('lending');
const route = useRoute();

const currentTab = route.query.activeTab;
if (currentTab && !Array.isArray(currentTab)) {
  if (currentTab === 'lending' || currentTab === 'renting') {
    activeTab.value = currentTab;
  }
}

navigateTo({ query: { activeTab: activeTab.value } }, { replace: true });

const tabs = [
  { id: 'lending', label: "Books I'm Lending", icon: 'lucide:trending-up' },
  { id: 'renting', label: "Books I'm Renting", icon: 'lucide:trending-down' },
] as const;

const headerText = computed(() => {
  return activeTab.value === 'lending' ? 'Lend Status' : 'Rent Status';
});

const updateUrl = (newActiveTab: string) => {
  const url = new URL(window.location.href);
  url.searchParams.set('activeTab', newActiveTab);
  window.history.replaceState({}, '', url.toString());
};

updateUrl(activeTab.value);

watch(activeTab, (val) => {
  updateUrl(val);
});
</script>

<template>
  <div class="flex flex-col min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mb-6 flex justify-between items-start">
      <div class="text-base">
        <h1 class="font-bold text-3xl flex items-center gap-2 mb-1">
          <Icon name="fluent:calendar-24-regular" class="w-8 h-8 text-orange-500" />
          My Rentals
        </h1>
        <p class="text-muted">Manage your lending and renting activities</p>
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
        :to="{ path: '/rentals/history', query: { activeTab } }"
        class="text-foreground font-medium flex items-center gap-1 cursor-pointer"
      >
        {{ activeTab === 'lending' ? 'Lend' : 'Rent' }} history
        <Icon name="lucide:move-right" class="w-6 h-6 text-foreground" />
      </NuxtLink>
    </div>

    <!-- Pass activeTab to RentalsSection as prop -->
    <RentalsSection :active-tab="activeTab" />
  </div>
</template>
