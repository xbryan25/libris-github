<script setup lang="ts">
interface Props {
  profile: Profile | null;
  loading: boolean;
  error: string | null;
  userId: string;
}

const props = defineProps<Props>();

const userId = props.userId;

const booksOwnedCount = ref(0);
const booksRentedCount = ref(0);
const booksBoughtCount = ref(0);

onMounted(async () => {
  const data = await useLibraryDetails(userId);
  booksOwnedCount.value = data.booksOwned ?? 0;
  booksRentedCount.value = data.booksRented ?? 0;
  booksBoughtCount.value = data.booksBought ?? 0;
});
</script>

<template>
  <div
    v-if="props.loading"
    class="w-full max-w-[1500px] h-auto bg-white dark:bg-zinc-950 border border-zinc-300 dark:border-zinc-800 border-radius rounded-lg flex flex-col items-stretch px-16 gap-8 py-6"
  >
    <USkeleton class="h-10 w-64" />

    <div class="flex-1 flex w-full items-stretch mb-8">
      <div class="flex-1 flex gap-x-10 w-full pr-20">
        <div class="flex-1 flex flex-col gap-2">
          <USkeleton class="h-8 w-45" />
          <USkeleton class="h-6 w-10" />
        </div>
        <div class="flex-1 flex flex-col gap-2">
          <USkeleton class="h-8 w-45" />
          <USkeleton class="h-6 w-10" />
        </div>
        <div class="flex-1 flex flex-col gap-2">
          <USkeleton class="h-8 w-45" />
          <USkeleton class="h-6 w-10" />
        </div>
      </div>

      <USkeleton class="flex-1 flex h-auto" />
    </div>
  </div>

  <div
    v-else-if="error"
    class="w-[1500px] h-[350px] bg-surface border-base flex items-center justify-center"
  >
    <div class="text-lg text-red-500">Error: {{ error }}</div>
  </div>

  <div
    v-else
    class="w-full max-w-[1500px] h-auto bg-white dark:bg-zinc-950 border border-zinc-300 dark:border-zinc-800 border-radius rounded-lg flex flex-col items-stretch px-16 py-6"
  >
    <div class="text-[32px] font-bold text-base pb-8">Library Details</div>

    <div class="flex-1 flex w-full items-stretch mb-8">
      <div class="flex-1 flex gap-x-10 w-full pr-20">
        <div class="flex-1 flex flex-col">
          <div class="text-[25px] font-semibold text-base">Owned Books</div>
          <div class="text-[20px] text-muted truncate max-w-full">{{ booksOwnedCount }}</div>
        </div>
        <div class="flex-1 flex flex-col">
          <div class="text-[25px] font-semibold text-base">Rented Books</div>
          <div class="text-[20px] text-muted truncate max-w-full">{{ booksRentedCount }}</div>
        </div>
        <div class="flex-1 flex flex-col">
          <div class="text-[25px] font-semibold text-base">Bought Books</div>
          <div class="text-[20px] text-muted truncate max-w-full">{{ booksBoughtCount }}</div>
        </div>
      </div>

      <NuxtLink
        :to="`/users/${userId}/collection`"
        class="flex-1 flex h-auto items-center justify-center font-bold text-2xl cursor-pointer bg-primary-600 rounded-xl"
      >
        <UTooltip :text="`View ${props.profile?.username || '-'}'s book collection`">
          <span
            class="truncate block max-w-[225px] sm:max-w-[325px] md:max-w-[375px] lg:max-w-[475px] xl:max-w-[525px] 2xl:max-w-[625px]"
          >
            View {{ props.profile?.username || '-' }}'s book collection
          </span>
        </UTooltip>
      </NuxtLink>
    </div>
  </div>
</template>
