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

const refreshTrigger = ref(0);

const isOpenAddBookModal = ref(false);

const openAddBookModal = () => {
  isOpenAddBookModal.value = true;
};

const onRefreshSignal = () => {
  refreshTrigger.value++; // this will change value each time
};
</script>

<template>
  <div class="flex flex-col items-center w-full min-h-screen pt-4 px-4 md:px-8 lg:px-15">
    <div class="flex w-full px-10 py-5">
      <div class="flex-1 flex flex-col gap-1">
        <div class="flex items-center gap-2">
          <Icon name="lucide:book-open" class="w-8 h-8 text-base" />
          <h1 class="font-bold text-3xl">My Library</h1>
        </div>

        <p class="text-muted">All your owned books, in one place.</p>
      </div>

      <div class="flex-1 flex justify-end pt-5">
        <UButton class="w-40 justify-center cursor-pointer" @click="openAddBookModal">
          <Icon name="material-symbols:add" class="w-8 h-8 text-bg" />
          <p class="font-bold text-xl">Add Book</p>
        </UButton>
      </div>
    </div>

    <BookListHeader
      :header-state="headerState"
      @update:search-value="(newSearchValue: string) => (headerState.searchValue = newSearchValue)"
      @update:selected-book-genre="
        (newSelectedBookAvailability: string) =>
          (headerState.selectedBookGenre = newSelectedBookAvailability)
      "
      @update:selected-book-availability="
        (newSelectedBookAvailability: string) =>
          (headerState.selectedBookAvailability = newSelectedBookAvailability)
      "
    />

    <MyLibraryBookList :header-state="headerState" :add-book-refresh-trigger="refreshTrigger" />

    <AddBookModal
      :is-open-add-book-modal="isOpenAddBookModal"
      @update:open-add-book-modal="
        (newIsOpenAddBookModal) => (isOpenAddBookModal = newIsOpenAddBookModal)
      "

      @add-book-success="onRefreshSignal"
    />
  </div>
</template>
