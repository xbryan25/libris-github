<script setup lang="ts">
import type { Book } from '~/types';

const booksData = ref<Book[]>([]);

const genreItems = ref(['All Genres', 'Horror', 'Fantasy', 'Action']);
const genreValue = ref('All Genres');

const statusItems = ref(['All', 'For Rent', 'For Sale', 'Both']);
const statusValue = ref('All');

const booksPerPage = ref(8);
const pageNumber = ref(1);

const searchValue = ref('');
const genre = ref('All Genres');
const availability = ref('All');

const loadBooks = async () => {
  const options = {
    booksPerPage: booksPerPage.value,
    pageNumber: pageNumber.value,
    searchValue: searchValue.value,
    genre: genre.value,
    availability: availability.value,
  };

  const data = await useBooks(options);

  booksData.value = data;
};

onMounted(async () => {
  await loadBooks();
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
        class="grid grid-cols-[repeat(auto-fit,minmax(225px,1fr))] place-items-center justify-center gap-2 h-full grid-rows-1 sm:grid-rows-[auto]"
      >
        <!-- <BookCard v-for="n in 10" :key="n" card-type="hasContent" />

        <BookCard v-for="n in 1" :key="n" card-type="empty" /> -->

        <BookCard
          v-for="book in booksData"
          :key="book.bookId"
          card-type="hasContent"
          :book-details="book"
        />

        <BookCard v-for="_ in 4" :key="_" card-type="empty" />
      </div>
    </div>

    <UPagination v-model:page="pageNumber" :total="100" class="py-5" />
  </div>
</template>
