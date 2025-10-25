<script setup lang="ts">
import type { Book } from '~/types';
import { useDebounceFn } from '@vueuse/core';

const props = defineProps<{
  headerState: {
    searchValue: string;
    selectedBookGenre: string;
    selectedBookAvailability: string;
  };
}>();

const booksData = ref<Book[]>([]);

const gridContainer = ref<HTMLElement | null>(null);

const cardWidth = 225;
const cardHeight = 400;

const booksPerPage = ref(1);
const pageNumber = ref(1);
const totalBookCount = ref(0);

const getGridCapacity = () => {
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
  };

  const data = await useBooksForBrowse(options);
  booksData.value = data;

  console.log(booksData.value);
};

const getTotalBookCount = async () => {
  const options = {
    searchValue: props.headerState.searchValue,
    bookGenre: props.headerState.selectedBookGenre,
    bookAvailability: props.headerState.selectedBookAvailability,
  };

  const { totalCount }: { totalCount: number } = await useTotalBookCount(options);

  totalBookCount.value = totalCount;
};

watch(
  () => pageNumber.value,
  async () => {
    isFetching.value = true;

    await debouncedLoadBooks();

    isFetching.value = false;
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
}, 700);

const debouncedLoadBookCount = useDebounceFn(async () => {
  await getTotalBookCount();

  checkIfBeyondPageLimit();
}, 700);

const handleResize = async () => {
  isFetching.value = true;

  await debouncedLoadBooks();
  await debouncedLoadBookCount();

  isFetching.value = false;
};

watch(
  [
    () => props.headerState.searchValue,
    () => props.headerState.selectedBookAvailability,
    () => props.headerState.selectedBookGenre,
  ],
  async () => {
    isFetching.value = true;

    await debouncedLoadBooks();
    await debouncedLoadBookCount();

    isFetching.value = false;
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
        class="grid grid-cols-[repeat(auto-fit,minmax(225px,1fr))] place-items-center justify-center gap-2 auto-rows-max min-h-[820px]"
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
