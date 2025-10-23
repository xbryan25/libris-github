<script setup lang="ts">
import type { Book } from '~/types';
import { useDebounceFn } from '@vueuse/core';

const booksData = ref<Book[]>([]);

const gridContainer = ref<HTMLElement | null>(null);

const cardWidth = 225;
const cardHeight = 400;

const genreItems = ref(['All Genres', 'Horror', 'Fantasy', 'Action']);
const genreValue = ref('All Genres');

const statusItems = ref(['All', 'For Rent', 'For Sale', 'Both']);
const statusValue = ref('All');

const booksPerPage = ref(1);
const pageNumber = ref(1);
const totalBookCount = ref(0);

const searchValue = ref('');
const genre = ref('All Genres');
const availability = ref('All');

function getGridCapacity() {
  if (!gridContainer.value) return 0;

  const width = gridContainer.value.offsetWidth;
  const height = gridContainer.value.offsetHeight;

  const gridGap = 8; // or whatever your Tailwind gap is in px
  const cols = Math.floor((width + gridGap) / (cardWidth + gridGap));

  const rows = Math.min(Math.floor(height / cardHeight), 2); // ✅ limit rows to 2 max

  // Actual visible cards
  const visibleCount = cols * rows;

  // Minimum of 2 rows
  const minCount = cols * 2;

  // Return whichever is greater
  return Math.max(visibleCount, minCount);
}

const isFetching = ref(false);

const loadBooks = async () => {
  if (isFetching.value) return;

  const capacity = getGridCapacity();
  if (capacity <= 0) return;

  isFetching.value = true;
  booksPerPage.value = capacity;
  console.log(`booksPerPage: ${booksPerPage.value}`);

  const options = {
    booksPerPage: booksPerPage.value,
    pageNumber: pageNumber.value,
    searchValue: searchValue.value,
    genre: genre.value,
    availability: availability.value,
  };

  const data = await useBooks(options);
  booksData.value = data;

  isFetching.value = false;
};

const getTotalBookCount = async () => {
  const options = {
    searchValue: searchValue.value,
    genre: genre.value,
    availability: availability.value,
  };

  const { totalCount }: { totalCount: number } = await useTotalBookCount(options);

  totalBookCount.value = totalCount;

  console.log(`total book count: ${totalBookCount.value}`);
};

watch(
  () => pageNumber.value,
  async () => {
    await debouncedLoadBooks();
  },
);

const checkIfBeyondPageLimit = () => {
  const totalPages = Math.ceil(totalBookCount.value / booksPerPage.value) || 1;

  // If current page exceeds total pages, clamp it down
  if (pageNumber.value > totalPages) {
    pageNumber.value = totalPages;

    console.log('reachhh heree?');
  }

  // If there are no records, reset to page 1
  if (totalBookCount.value === 0) {
    pageNumber.value = 1;
  }
};

const debouncedLoadBooks = useDebounceFn(async () => {
  await loadBooks();
}, 300);

const debouncedLoadBookCount = useDebounceFn(async () => {
  await getTotalBookCount();

  checkIfBeyondPageLimit();
}, 300);

const handleResize = async () => {
  await debouncedLoadBooks();
  await debouncedLoadBookCount();
};

onMounted(async () => {
  await debouncedLoadBooks();
  await debouncedLoadBookCount();

  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<template>
  <div class="h-full w-full flex flex-col items-center px-10">
    <div class="mt-5 p-5 bg-surface-hover rounded-lg w-full">
      <div class="flex gap-5">
        <UInput
          icon="i-lucide-search"
          size="xl"
          variant="outline"
          placeholder="Search books..."
          class="flex-[4] bg-surface-hover"
        />
        <USelectMenu v-model="genreValue" :items="genreItems" size="xl" class="flex-1" />
        <USelectMenu v-model="statusValue" :items="statusItems" size="xl" class="flex-1" />
      </div>
    </div>

    <div class="flex-1 pt-5 w-full">
      <div
        ref="gridContainer"
        class="grid grid-cols-[repeat(auto-fit,minmax(225px,1fr))] place-items-center justify-center gap-2 auto-rows-max"
      >
        <BookCard
          v-for="book in booksData"
          :key="book.bookId"
          card-type="hasContent"
          :book-details="book"
        />

        <BookCard
          v-for="_ in Math.max(0, booksPerPage - booksData.length)"
          :key="_"
          card-type="empty"
        />
      </div>
    </div>

    <UPagination
      v-model:page="pageNumber"
      :items-per-page="booksPerPage"
      show-edges
      :sibling-count="0"
      :total="totalBookCount"
      class="py-5"
    />
  </div>
</template>
