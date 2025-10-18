<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});

</script>

<template>
<div class="flex flex-col justify-start items-start h-screen w-screen mt-4 ml-15">
  <div class="text-[42px] font-bold text-base">Welcome back, xbryan 25!</div>
  <div class="text-sm text-muted ml-1">Here’s your activity overview.</div>

  <div class="flex justify-center w-full mt-4">
  <div class="grid grid-cols-6 gap-6 mt-4">
    <UCard class="w-[250px] h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
      <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
      <div class="text-2xl font-bold mt-2">12</div>
      <div class="text-sm text-neutral mt-1">Books Borrowed</div>
    </UCard>

    <UCard class="w-[250px] h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
      <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
      <div class="text-2xl font-bold mt-2">5</div>
      <div class="text-sm text-neutral mt-1">Currently Lending</div>
    </UCard>

    <UCard class="w-[250px] h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
      <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
      <div class="text-2xl font-bold mt-2">3</div>
      <div class="text-sm text-neutral mt-1">Currently Renting</div>
    </UCard>

    <UCard class="w-[250px] h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
      <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
      <div class="text-2xl font-bold mt-2">8</div>
      <div class="text-sm text-neutral mt-1">Books Sold</div>
    </UCard>

    <UCard class="w-[250px] h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
      <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
      <div class="text-2xl font-bold mt-2">6</div>
      <div class="text-sm text-neutral mt-1">Books Bought</div>
    </UCard>

    <UCard class="w-[250px] h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
      <Icon name="fluent:book-coins-20-regular" class="text-5xl text-accent" />
      <div class="text-2xl font-bold mt-2">10</div>
      <div class="text-sm text-neutral mt-1">Total Earnings</div>
    </UCard>
  </div>
</div>
</div>
</template>
