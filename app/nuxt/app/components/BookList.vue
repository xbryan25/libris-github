<script setup lang="ts">
import type { Book } from '~/types';
import { useDebounceFn } from '@vueuse/core';

interface PriceRange {
  minPrice: number | null;
  maxPrice: number | null;
}

const props = defineProps<{
  headerState: {
    searchValue: string;
    selectedBookGenre: string;
    selectedBookAvailability: string;
    selectedPriceRange: PriceRange;
    kmRadius: number | null;
    userLat: number | null;
    userLng: number | null;
  };
  userId?: string;
}>();


const booksData = ref<Book[]>([]);

const gridContainer = ref<HTMLElement | null>(null);

const cardWidth = 225;

const booksPerPage = ref(1);
const pageNumber = ref(1);
const totalBookCount = ref(0);

const getGridCapacity = () => {
  const el = gridContainer.value;
  if (!el) return 0;

  const width = el.clientWidth;
  const gridGap = 12;
  const cols = Math.max(1, Math.floor((width + gridGap) / (cardWidth + gridGap)));

  const rows = 2;

  const total = cols * rows;

  return total;
};

const isFetching = ref(false);

const loadBooks = async () => {
  const capacity = getGridCapacity();
  if (capacity <= 0) return;

  booksPerPage.value = capacity;

  const options = {
    booksPerPage: booksPerPage.value,
    pageNumber: pageNumber.value,
    searchValue: props.headerState.searchValue,
    bookGenre: props.headerState.selectedBookGenre,
    bookAvailability: props.headerState.selectedBookAvailability,
    userId: props.userId,
    minPrice: props.headerState.selectedPriceRange.minPrice,
    maxPrice: props.headerState.selectedPriceRange.maxPrice,
    kmRadius: props.headerState.kmRadius,
    userLat: props.headerState.userLat,
    userLng: props.headerState.userLng,
  };

  const data = await useBooksForBookList(options);
  booksData.value = data;
};

const getTotalBookCount = async () => {
  const options = {
    searchValue: props.headerState.searchValue,
    bookGenre: props.headerState.selectedBookGenre,
    bookAvailability: props.headerState.selectedBookAvailability,
    userId: props.userId,
    minPrice: props.headerState.selectedPriceRange.minPrice,
    maxPrice: props.headerState.selectedPriceRange.maxPrice,
    kmRadius: props.headerState.kmRadius,
    userLat: props.headerState.userLat,
    userLng: props.headerState.userLng,
  };

  const { totalCount }: { totalCount: number } = await useTotalBookCountForBookList(options);

  totalBookCount.value = totalCount;
};

const checkIfBeyondPageLimit = () => {
  const totalPages = Math.ceil(totalBookCount.value / booksPerPage.value) || 1;

  // If current page exceeds total pages, clamp it down
  if (pageNumber.value > totalPages) {
    pageNumber.value = totalPages;
  }

  // If there are no records, reset to page 1
  if (totalBookCount.value === 0) {
    pageNumber.value = 1;
  }
};

const debouncedLoadBooks = useDebounceFn(async () => {
  await loadBooks();
}, 700);

const debouncedLoadBookCount = useDebounceFn(async () => {
  await getTotalBookCount();

  checkIfBeyondPageLimit();
}, 700);

let lastCapacity = 0;

const handleResize = useDebounceFn(async () => {
  await nextTick();
  await new Promise((resolve) => requestAnimationFrame(resolve));
  await new Promise((resolve) => setTimeout(resolve, 80));

  const newCapacity = getGridCapacity();
  if (newCapacity === lastCapacity || newCapacity <= 0) return;

  lastCapacity = newCapacity;

  isFetching.value = true;
  try {
    await loadBooks();
    checkIfBeyondPageLimit();
  } finally {
    isFetching.value = false;
  }
}, 400);

const refreshBooksData = useDebounceFn(async () => {
  try {
    await loadBooks();
    await getTotalBookCount();
  } catch (err) {
    console.error('Error loading books:', err);
  } finally {
    isFetching.value = false;
  }
}, 700);

watch(
  [
    () => props.headerState.searchValue,
    () => props.headerState.selectedBookAvailability,
    () => props.headerState.selectedBookGenre,
    () => props.headerState.selectedPriceRange,
    () => props.headerState.kmRadius, 
    () => props.headerState.userLat,
    () => props.headerState.userLng, 
  ],
  () => {
    isFetching.value = true; 
    pageNumber.value = 1; 
    
    refreshBooksData(); 
  },
  { deep: true },
);

watch(
  () => pageNumber.value,
  async () => {
    isFetching.value = true;

    try {
      await loadBooks(); 
    } catch (err) {
      console.error('Error changing page:', err);
    } finally {
      isFetching.value = false;
    }
  },
);

onMounted(async () => {
  isFetching.value = true;

  await debouncedLoadBooks();
  await debouncedLoadBookCount();

  isFetching.value = false;

  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<template>
  <div class="h-full w-full flex flex-col items-center">
    <div class="flex-1 pt-5 w-full relative">
      <div
        v-if="isFetching"
        class="absolute inset-0 flex justify-center items-center bg-background z-5"
      >
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
        <span class="ml-2 text-muted">Loading books...</span>
      </div>

      <div
        v-if="!isFetching && booksData.length == 0"
        class="absolute inset-0 flex justify-center items-center bg-background z-5"
      >
        <UIcon name="heroicons:x-mark-16-solid" class="w-12 h-12 animate-bounce text-accent" />
        <span class="ml-2 text-muted">No books here...</span>
      </div>

      <div
        ref="gridContainer"
        class="grid grid-cols-[repeat(auto-fit,minmax(225px,1fr))] gap-3"
        style="
          grid-auto-rows: 400px;
          max-height: calc(400px * 2 + 12px);
          min-height: calc(400px * 2 + 12px);
          overflow: hidden;
        "
      >
        <BookListCard
          v-for="book in booksData"
          :key="book.bookId"
          card-type="hasContent"
          :book-details="book"
        />

        <BookListCard
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
