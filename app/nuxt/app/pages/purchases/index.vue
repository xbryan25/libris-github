<script setup lang="ts">
import auth from '~/middleware/auth';
import PurchasesSection from '~/components/PurchasesSection.vue';
import { ref, computed } from 'vue';

definePageMeta({
  middleware: auth,
});

const activeTab = ref<'selling' | 'buying'>('selling');
const route = useRoute();

const currentTab = route.query.activeTab;
if (currentTab && !Array.isArray(currentTab)) {
  if (currentTab === 'selling' || currentTab === 'buying') {
    activeTab.value = currentTab;
  }
}

const tabs = [
  { id: 'selling', label: "Books I'm Selling", icon: 'lucide:trending-up' },
  { id: 'buying', label: 'Books Buy Request', icon: 'lucide:trending-down' },
] as const;

const headerText = computed(() => {
  return activeTab.value === 'selling' ? 'Sell Status' : 'Buy Status';
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
          My Purchases
        </h1>
        <p class="text-muted">Manage your purchasing and selling activities</p>
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
        :to="{ path: '/purchases/history', query: { activeTab } }"
        class="text-foreground font-medium flex items-center gap-1 cursor-pointer"
      >
        {{ activeTab === 'selling' ? 'Sell' : 'Purchase' }} history
        <Icon name="lucide:move-right" class="w-6 h-6 text-foreground" />
      </NuxtLink>
    </div>

    <!-- Pass activeTab to PurchasesSection as prop -->
    <PurchasesSection :active-tab="activeTab" />
  </div>
</template>
