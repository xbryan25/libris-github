<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import DashboardBookCard from './DashboardBookCard.vue';
import { useBooks } from '~/composables/useUserBooks';

const { booksData, loading, error, fetchBooksData } = useBooks();

const activeTab = ref<'renting' | 'bought' | 'rented-by-others' | 'bought-by-others'>('renting');

const tabs = [
  { id: 'renting', label: "Books I'm Renting", icon: 'lucide:book-open' },
  { id: 'bought', label: 'Books I Bought', icon: 'ph:magnifying-glass-bold' },
  { id: 'rented-by-others', label: "Books I'm Lending", icon: 'ci-calendar' },
  { id: 'bought-by-others', label: "Books I've Sold", icon: 'ci-calendar' },
] as const;

const currentSection = computed(() => {
  return tabs.find((tab) => tab.id === activeTab.value) || tabs[0];
});

const currentBooks = computed(() => {
  return booksData.value[activeTab.value] || [];
});

const getEmptyStateMessage = (tab: string) => {
  const messages: Record<string, string> = {
    renting: "You haven't rented any books yet. Start exploring available books!",
    bought: "You haven't purchased any books yet. Check out our collection!",
    'rented-by-others': 'No one is renting your books yet. List more books to get started!',
    'bought-by-others': "You haven't sold any books yet. List your books for sale!",
  };
  return messages[tab] || 'No books found in this section';
};

onMounted(() => {
  fetchBooksData();
});
</script>

<template>
  <div class="w-full bg-background">
    <!-- Navigation Tabs -->
    <div class="mx-auto">
      <div v-if="loading" class="grid grid-cols-4 gap-3">
        <USkeleton class="h-10 w-full" />
        <USkeleton class="h-10 w-full" />
        <USkeleton class="h-10 w-full" />
        <USkeleton class="h-10 w-full" />
      </div>

      <div v-else class="grid grid-cols-4 gap-3">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :disabled="loading"
          :class="[
            'px-4 py-3 rounded-lg font-medium transition-all text-center cursor-pointer',
            activeTab === tab.id
              ? 'bg-accent text-white'
              : 'bg-surface text-foreground hover:bg-surface-hover',
          ]"
          @click="activeTab = tab.id"
        >
          <div class="flex items-center gap-1">
            <Icon :name="tab.icon" />
            <span class="text-sm leading-tight">{{ tab.label }}</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12 h-87">
      <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
      <span class="ml-2 text-muted">Loading books...</span>
    </div>

    <!-- Books Section -->
    <div v-else class="w-full">
      <div class="mx-auto py-7">
        <div class="bg-surface rounded-lg p-6 w-full border border-base">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-semibold flex items-center gap-3">
              <Icon :name="currentSection.icon" />
              <span class="text-3xl">{{ currentSection.label }}</span>
            </h2>
            <button
              v-if="currentBooks.length > 0"
              class="px-4 py-2 bg-surface-hover hover:bg-accent hover:text-white rounded-md font-medium cursor-pointer transition-colors"
            >
              See more
            </button>
          </div>

          <!-- Empty State -->
          <div v-if="currentBooks.length === 0" class="text-center py-12">
            <UIcon name="i-heroicons-book-open" class="w-16 h-16 text-muted mx-auto" />
            <p class="text-muted mt-4 text-lg">No books found in this section</p>
            <p class="text-sm text-muted mt-2">{{ getEmptyStateMessage(activeTab) }}</p>
          </div>

          <!-- Books Carousel -->
          <UCarousel
            v-else
            v-slot="{ item }"
            :items="currentBooks"
            :ui="{
              item: 'basis-full sm:basis-1/2 md:basis-1/3 lg:basis-1/4 xl:basis-1/5 2xl:basis-1/6',
            }"
            arrows
            class="w-full"
          >
            <DashboardBookCard :book="item" :type="activeTab" class="mx-2" />
          </UCarousel>
        </div>
      </div>
    </div>
  </div>
</template>
