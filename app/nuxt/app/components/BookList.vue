<script setup lang="ts">
const genreItems = ref(['All Genres', 'Horror', 'Fantasy', 'Action']);
const genreValue = ref('All Genres');

const statusItems = ref(['For Rent', 'For Sale', 'Both']);
const statusValue = ref('For Rent');

const cards = ref([
  {
    title: 'Icons',
    description: 'Nuxt UI integrates with Nuxt Icon to access over 200,000+ icons from Iconify.',
    icon: 'i-lucide-smile',
    to: '/docs/getting-started/integrations/icons',
  },
  {
    title: 'Fonts',
    description: 'Nuxt UI integrates with Nuxt Fonts to provide plug-and-play font optimization.',
    icon: 'i-lucide-a-large-small',
    to: '/docs/getting-started/integrations/fonts',
  },
  {
    title: 'Color Mode',
    description: 'Nuxt UI integrates with Nuxt Color Mode to switch between light and dark.',
    icon: 'i-lucide-sun-moon',
    to: '/docs/getting-started/integrations/color-mode',
  },
]);
</script>

<template>
  <div class="w-full flex flex-col px-10">
    <div class="mt-5 p-5 bg-surface-hover rounded-lg">
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

    <div class="h-auto py-5">
      <div
        class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] place-items-center justify-center gap-4 h-full grid-rows-1 sm:grid-rows-[auto]"
      >
        <BookCard v-for="n in 8" :key="n" />
      </div>
    </div>
  </div>
</template>

<!-- <div class="flex-1 grid grid-rows-2 grid-cols-5 place-items-center gap-4">
        <PetCard
          v-for="pet in petList"
          :key="pet.petId"
          :name="pet.name"
          :status="pet.status"
          :petFirstImageUrl="pet.petFirstImageUrl"
          :petId="pet.petId"
          :petShelter="pet.petShelter"
          :isNotDummy="true"
        />

        <PetCard v-for="_ in dummyFramesToLoad" :key="_" :isNotDummy="false" />
      </div> -->
