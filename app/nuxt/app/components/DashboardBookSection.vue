<template>
  <div class="w-full bg-background">
    <!-- Navigation Tabs -->
    <div class="mx-auto">
      <div class="grid grid-cols-4 gap-3">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-4 py-3 rounded-lg font-medium transition-all text-center cursor-pointer',
            activeTab === tab.id
              ? 'bg-accent text-white'
              : 'bg-surface text-foreground hover:bg-surface-hover'
          ]"
        >
          <div class="flex items-center gap-1">
            <Icon :name="tab.icon"/>
            <span class="text-sm leading-tight">{{ tab.label }}</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Books Section -->
    <div class="w-full">
      <div class="mx-auto py-7">
        <div class="bg-surface rounded-lg p-6 w-full border border-base">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-semibold flex items-center gap-3">
              <Icon :name="currentSection.icon" />
              <span class="text-3xl">{{ currentSection.label }}</span>
            </h2>
            <button class="px-4 py-2 bg-surface-hover hover:bg-accent hover:text-white rounded-md font-medium cursor-pointer transition-colors">
              See more
            </button>
          </div>

          <!-- Books Carousel -->
          <UCarousel
            v-slot="{ item }"
            :items="currentBooks"
            :ui="{
              item: 'basis-full sm:basis-1/2 md:basis-1/3 lg:basis-1/4 xl:basis-1/5 2xl:basis-1/6'
            }"
            arrows
            class="w-full"
          >
            <DashboardBookCard
              :book="item"
              :type="activeTab"
              class="mx-2"
            />
          </UCarousel>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import DashboardBookCard from './DashboardBookCard.vue'

const activeTab = ref('renting')

const tabs = [
  { id: 'renting', label: "Books I'm Renting", icon: 'lucide:book-open' },
  { id: 'bought', label: 'Books I Bought', icon: 'ph:magnifying-glass-bold' },
  { id: 'rented-by-others', label: "Books I'm Lending", icon: 'ci-calendar' },
  { id: 'bought-by-others', label: "Books I've Sold", icon: 'ci-calendar' }
]

// Sample data for each section
const booksData = {
  renting: [
    {
      id: 1,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    },
    {
      id: 2,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    },
    {
      id: 3,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    },
    {
      id: 4,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    },
    {
      id: 5,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    },
    {
      id: 6,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    },
    {
      id: 7,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    }
  ],
  bought: [
    {
      id: 4,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://m.media-amazon.com/images/I/61M+d+buZVL._SL1500_.jpg',
      from: 'xbryan25',
      cost: '50'
    }
  ],
  'rented-by-others': [
    {
      id: 5,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
      by: 'xbryan25',
      returnDate: 'October 1, 2025',
      cost: '50'
    }
  ],
  'bought-by-others': [
    {
      id: 6,
      title: 'The Passion Within',
      author: 'J.K. Rowling',
      image: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
      by: 'xbryan25',
      cost: '50'
    }
  ]
}

const currentSection = computed(() => {
  return tabs.find(tab => tab.id === activeTab.value)
})

const currentBooks = computed(() => {
  return booksData[activeTab.value] || []
})
</script>