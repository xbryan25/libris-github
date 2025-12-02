<script setup lang="ts">
import auth from '~/middleware/auth';
import { ref, computed } from 'vue';

definePageMeta({
  middleware: auth,
});

const activeTab = ref<'selling' | 'buying'>('buying');
const route = useRoute();

const currentTab = route.query.activeTab;
if (currentTab && !Array.isArray(currentTab)) {
  if (currentTab === 'selling' || currentTab === 'buying') {
    activeTab.value = currentTab;
  }
}

navigateTo({ query: { activeTab: activeTab.value } }, { replace: true });

const tabs = [
  { id: 'selling', label: "Books I'm Selling", icon: 'lucide:trending-up' },
  { id: 'buying', label: 'Books Buy Request', icon: 'lucide:trending-down' },
] as const;

const headerText = computed(() => {
  return activeTab.value === 'selling' ? 'Sell History' : 'Purchase History';
});

const sortByItems = ref(['Start date', 'End date']);
const sortOrderItems = ref(['newest first', 'oldest first']);
const cardsPerPageItems = ref([10, 25, 50]);

const sortBy = ref('Start date');
const sortOrder = ref('newest first');
const cardsPerPage = ref(10);

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
  <div class="flex flex-col h-auto w-full pt-4 px-4 md:px-8 lg:px-15">
    <div class="mb-6 flex justify-between items-start">
      <div class="text-base">
        <h1 class="font-bold text-3xl flex items-center gap-2 mb-1">
          <Icon name="fluent:calendar-24-regular" class="w-8 h-8 text-orange-500" />
          My Sell And Purchase History
        </h1>
        <p class="text-muted">See your selling and buying activity</p>
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

    <div class="flex mb-6">
      <h2 class="flex-1 text-xl font-bold text-foreground">{{ headerText }}</h2>

      <div class="flex-[3] flex justify-center gap-2">
        <div class="flex items-center gap-2">
          <p>Sort by</p>
          <USelect v-model="sortBy" :items="sortByItems" class="w-45" />
        </div>

        <USeparator orientation="vertical" color="primary" size="sm" />

        <div class="flex items-center gap-2">
          <p>Show</p>
          <USelect v-model="sortOrder" :items="sortOrderItems" class="w-45" />
        </div>

        <USeparator orientation="vertical" color="primary" size="sm" />

        <div class="flex items-center gap-2">
          <USelect v-model="cardsPerPage" :items="cardsPerPageItems" class="w-20" />
          <p>cards per page</p>
        </div>
      </div>

      <div class="flex-1 flex justify-end items-center">
        <NuxtLink
          :to="{ path: '/rentals', query: { activeTab } }"
          class="text-foreground font-medium flex gap-1 cursor-pointer"
        >
          Current {{ activeTab === 'selling' ? 'sold' : 'purchases' }}
          <Icon name="lucide:move-right" class="w-6 h-6 text-foreground" />
        </NuxtLink>
      </div>
    </div>

    <!-- Pass activeTab to RentalsHistorySection as prop -->
    <PurchasesHistorySection
      :sort-by="sortBy"
      :sort-order="sortOrder"
      :cards-per-page="cardsPerPage"
      :active-tab="activeTab"
    />
  </div>
</template>
