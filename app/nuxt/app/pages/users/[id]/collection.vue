<!--NOTE: This collection is copied FROM 'browse.vue' for testing purposes. Replace or modify this page collection with proper filters - Sam-->

<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});

const headerState = reactive({
  searchValue: '',
  selectedBookGenre: 'All Genres',
  selectedBookAvailability: 'All',
});
</script>

<template>
  <div
    class="flex flex-col items-center justify-center w-full min-h-screen pt-4 px-4 md:px-8 lg:px-15"
  >
    <BookListHeader
      :header-state="headerState"
      @update:search-value="(newSearchValue) => (headerState.searchValue = newSearchValue)"
      @update:selected-book-genre="
        (newSelectedBookAvailability) =>
          (headerState.selectedBookGenre = newSelectedBookAvailability)
      "
      @update:selected-book-availability="
        (newSelectedBookAvailability) =>
          (headerState.selectedBookAvailability = newSelectedBookAvailability)
      "
    />
    <BookList :header-state="headerState" />
  </div>
</template>
