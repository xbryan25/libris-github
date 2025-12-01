<script setup lang="ts">
import auth from '~/middleware/auth';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  middleware: auth,
});

interface PriceRange {
    minPrice: number | null;
    maxPrice: number | null;
}

const headerState = reactive({
  searchValue: '',
  selectedBookGenre: 'All Genres',
  selectedBookAvailability: 'All',
  selectedPriceRange: { 
        minPrice: null, 
        maxPrice: null 
    } as PriceRange,
    mileRadius: null as number | null,
});

const handlePriceRangeUpdate = (newPriceRange: PriceRange) => {
    headerState.selectedPriceRange = newPriceRange;
}

const handleMileRadiusUpdate = (newRadius: number | null) => {
    headerState.mileRadius = newRadius;
}

const authStore = useAuthStore();

const refreshTrigger = ref(0);

const isOpenAddBookModal = ref(false);

const totalBookCount = ref(0);
const isFetchingTotalBookCount = ref(true);

const openAddBookModal = () => {
  isOpenAddBookModal.value = true;
};

const onRefreshSignal = async () => {
  if (totalBookCount.value == 0) {
    isFetchingTotalBookCount.value = true;

    await getTotalBookCount();
  }

  refreshTrigger.value++;
};

const onRefreshSignalWhenDeleting = async () => {
  await getTotalBookCount();
};

const getTotalBookCount = async () => {
  const options = {
    searchValue: '',
    bookGenre: 'All Genres',
    bookAvailability: 'All',
    userId: authStore.user_id,
  };

  const { totalCount }: { totalCount: number } = await useTotalCountForMyLibrary(options);

  totalBookCount.value = totalCount;

  isFetchingTotalBookCount.value = false;
};

onMounted(async () => {
  await getTotalBookCount();
});
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

    <div v-if="totalBookCount > 0" class="w-full">
      <BookListHeader
        :header-state="headerState"
        :is-library-mode="true"
        @update:search-value="
          (newSearchValue: string) => (headerState.searchValue = newSearchValue)
        "
        @update:selected-book-genre="
          (newSelectedBookAvailability: string) =>
            (headerState.selectedBookGenre = newSelectedBookAvailability)
        "
        @update:selected-book-availability="
          (newSelectedBookAvailability: string) =>
            (headerState.selectedBookAvailability = newSelectedBookAvailability)
        "
        @update:selected-price-range="handlePriceRangeUpdate"
        @update:mile-radius="handleMileRadiusUpdate"
      />

      <MyLibraryBookList
        :header-state="headerState"
        :add-book-refresh-trigger="refreshTrigger"
        @delete-book-success="onRefreshSignalWhenDeleting"
      />
    </div>

    <div v-else-if="isFetchingTotalBookCount" class="h-80" />

    <div
      v-else
      class="w-full bg-surface-hover h-80 rounded-xl border border-zinc-400 dark:border-zinc-700 mt-5 flex items-center justify-center"
    >
      <div class="flex flex-col items-center gap-3">
        <Icon name="material-symbols:book-2" class="w-20 h-20 text-bg" />

        <div class="flex flex-col items-center">
          <h2 class="text-2xl font-bold">No books yet</h2>
          <p class="text-muted">Start building your library by adding your first book.</p>
        </div>

        <UButton class="justify-center cursor-pointer" @click="openAddBookModal">
          <Icon name="material-symbols:add" class="w-8 h-8 text-bg" />
          <p class="font-bold text-xl">Add Your First Book</p>
        </UButton>
      </div>
    </div>

    <AddBookModal
      :is-open-add-book-modal="isOpenAddBookModal"
      @update:open-add-book-modal="
        (newIsOpenAddBookModal) => (isOpenAddBookModal = newIsOpenAddBookModal)
      "
      @add-book-success="onRefreshSignal"
    />
  </div>
</template>
