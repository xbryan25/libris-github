<script setup lang="ts">
const genreItems = ref(['All Genres', 'Horror', 'Fantasy', 'Action']);
const genreValue = ref('All Genres');

const statusItems = ref(['For Rent', 'For Sale', 'Both']);
const statusValue = ref('For Rent');
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

    <div ref="elementRef" class="flex-1 py-5 w-full">
      <div
        class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] place-items-center justify-center gap-4 h-full grid-rows-1 sm:grid-rows-[auto]"
      >
        <BookCard v-for="n in 3" :key="n" card-type="hasContent" />

        <BookCard v-for="n in 2" :key="n" card-type="empty" />
      </div>
    </div>

    <UPagination v-model:page="page" :total="100" class="pt-5" />
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
