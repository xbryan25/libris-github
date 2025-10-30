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

const route = useRoute();
const userId = route.params.id as string;
const username = ref<string>('-');

const isFetching = ref(true);

onMounted(async () => {
  isFetching.value = true;

  const data = await useUsernameFromUserId(userId);
  username.value = data.username ?? '[ERROR]';

  isFetching.value = false;
});
</script>

<template>
  <div class="flex flex-col items-center w-full min-h-screen pt-4 px-4 md:px-8 lg:px-15">
    <div class="flex w-full pt-5 pb-5">
      <USkeleton v-if="isFetching" class="h-6 w-60" />

      <NuxtLink v-else :to="`/users/${userId}`" class="flex gap-2 cursor-pointer">
        <Icon name="material-symbols:arrow-back-rounded" class="w-5 h-5" />
        <span>Back to {{ username }}'s profile</span>
      </NuxtLink>
    </div>

    <div class="flex w-full px-5">
      <div class="flex-1 flex flex-col gap-1">
        <USkeleton v-if="isFetching" class="h-10 w-125" />

        <div v-else class="flex items-center gap-2">
          <Icon name="material-symbols:book-2-outline-rounded" class="w-8 h-8 text-base" />
          <h1 class="font-bold text-3xl">{{ username }}'s Book Collection</h1>
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
    />
    <BookList :header-state="headerState" :user-id="userId" />
  </div>
</template>
