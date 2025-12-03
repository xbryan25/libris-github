<script setup lang="ts">
import auth from '~/middleware/auth';

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
  kmRadius: null as number | null,
  userLat: null as number | null,
  userLng: null as number | null,
});

const currentWalletBalance = ref(0);
const isFetching = ref(true);

onMounted(async () => {
  isFetching.value = true;

  const data = await useCurrentWalletBalance();
  currentWalletBalance.value = data.currentWalletBalance ?? 0;

  // Get user's location from profile
  const { profile, fetchProfile } = useProfile();
  if (!profile.value) {
    await fetchProfile();
  }
  
  if (profile.value?.address?.latitude && profile.value?.address?.longitude) {
    headerState.userLat = profile.value.address.latitude;
    headerState.userLng = profile.value.address.longitude;
  }

  isFetching.value = false;
});
</script>

<template>
  <div class="flex flex-col items-center w-full min-h-screen pt-4 px-4 md:px-8 lg:px-15">
    <div v-if="isFetching" class="flex w-full px-10 py-5">
      <div class="flex-1 flex flex-col gap-2">
        <USkeleton class="h-9 w-60" />
        <USkeleton class="h-5 w-90" />
      </div>

      <div class="flex-1 flex flex-col items-end gap-1">
        <USkeleton class="h-5 w-25" />
        <USkeleton class="h-9 w-20" />
      </div>
    </div>

    <div v-else class="flex w-full px-10 py-5">
      <div class="flex-1 flex flex-col gap-1">
        <div class="flex items-center gap-2">
          <Icon name="material-symbols:search" class="w-8 h-8 text-base" />
          <h1 class="font-bold text-3xl">Browse Books</h1>
        </div>

        <p class="text-muted">Discover and rent books from the community.</p>
      </div>

      <div class="flex-1 flex flex-col items-end gap-1">
        <p class="text-muted">Your Readits</p>

        <div class="flex items-center gap-2">
          <Icon name="fluent:book-coins-20-regular" class="w-8 h-8 text-accent" />

          <h1 v-if="isFetching" class="font-bold text-3xl text-accent">-</h1>
          <h1 v-else class="font-bold text-3xl text-accent">{{ currentWalletBalance }}</h1>
        </div>
      </div>
    </div>

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
      @update:selected-price-range="
        (newPriceRange: PriceRange) => (headerState.selectedPriceRange = newPriceRange)
      "
      @update:km-radius="(newkmRadius: number | null) => (headerState.kmRadius = newkmRadius)"
    />

    <BookList book-list-variant="default" :header-state="headerState" />
  </div>
</template>
