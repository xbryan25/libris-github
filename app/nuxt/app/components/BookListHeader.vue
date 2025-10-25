<script setup lang="ts">
import { useBookGenres } from '~/composables/useBookGenres';

const props = defineProps<{
  headerState: {
    searchValue: string;
    selectedBookGenre: string;
    selectedBookAvailability: string;
  };
}>();

const emit = defineEmits<{
  (
    e: 'update:searchValue' | 'update:selectedBookGenre' | 'update:selectedBookAvailability',
    value: string,
  ): void;
}>();

const searchValue = ref(props.headerState.searchValue);

const bookGenreItems = ref(['All Genres']);
const bookGenreValue = ref(props.headerState.selectedBookGenre);

const bookAvailabilityItems = ref(['All', 'For Rent', 'For Sale', 'Both']);
const bookAvailabilityValue = ref(props.headerState.selectedBookAvailability);

const loadBookGenreItems = async () => {
  const bookGenres = await useBookGenres();

  bookGenreItems.value = ['All Genres', ...bookGenres];
};

watch(
  () => searchValue.value,
  (newSearchValue) => emit('update:searchValue', newSearchValue),
);

watch(
  () => bookGenreValue.value,
  (newBookGenreValue) => emit('update:selectedBookGenre', newBookGenreValue),
);

watch(
  () => bookAvailabilityValue.value,
  (newBookAvailabilityValue) => emit('update:selectedBookAvailability', newBookAvailabilityValue),
);

onMounted(async () => {
  await loadBookGenreItems();
});
</script>

<template>
  <div class="mt-5 p-5 bg-surface-hover rounded-lg w-full">
    <div class="flex gap-5">
      <UInput
        v-model="searchValue"
        icon="i-lucide-search"
        size="xl"
        variant="outline"
        placeholder="Search books..."
        class="flex-[4] bg-surface-hover"
      />
      <USelectMenu v-model="bookGenreValue" :items="bookGenreItems" size="xl" class="flex-1" />
      <USelectMenu
        v-model="bookAvailabilityValue"
        :items="bookAvailabilityItems"
        size="xl"
        class="flex-1"
      />
    </div>
  </div>
</template>
