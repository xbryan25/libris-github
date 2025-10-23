<script setup lang="ts">
import DashboardBookSection from '~/components/DashboardBookSection.vue';
import auth from '~/middleware/auth';
import { onMounted } from 'vue'
import { useDashboard } from '~/composables/useDashboard'

definePageMeta({
  middleware: auth,
});

const { summary, username, fetchAll, loading, error } = useDashboard()

onMounted(() => {
  fetchAll()
})

</script>

<template>
<div class="flex flex-col min-h-screen w-full pt-4 px-4 md:px-8 lg:px-15">
  <div class="text-[42px] font-bold text-base">Welcome back, {{username}}!</div>
  <div class="text-sm text-muted ml-1">Here’s your activity overview.</div>

  <div class="w-full mt-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-6">
      <UCard class="h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
        <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
        <div class="text-2xl font-bold mt-2">{{summary.books_borrowed}}</div>
        <div class="text-sm text-neutral mt-1">Books Borrowed</div>
      </UCard>

      <UCard class="w-full h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
        <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
        <div class="text-2xl font-bold mt-2">{{summary.currently_lending}}</div>
        <div class="text-sm text-neutral mt-1">Currently Lending</div>
      </UCard>

      <UCard class="w-full h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
        <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
        <div class="text-2xl font-bold mt-2">{{summary.currently_renting}}</div>
        <div class="text-sm text-neutral mt-1">Currently Renting</div>
      </UCard>

      <UCard class="w-full h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
        <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
        <div class="text-2xl font-bold mt-2">{{summary.books_sold}}</div>
        <div class="text-sm text-neutral mt-1">Books Sold</div>
      </UCard>

      <UCard class="w-full h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
        <UIcon name="i-heroicons-book-open" class="text-5xl text-[#3B82F6]" />
        <div class="text-2xl font-bold mt-2">{{summary.books_bought}}</div>
        <div class="text-sm text-neutral mt-1">Books Bought</div>
      </UCard>

      <UCard class="w-full h-[170px] text-center flex flex-col items-center justify-center bg-surface border-base">
        <Icon name="fluent:book-coins-20-regular" class="text-5xl text-accent" />
        <div class="text-2xl font-bold mt-2">{{summary.total_earnings}}</div>
        <div class="text-sm text-neutral mt-1">Total Earnings</div>
      </UCard>
    </div>
    <DashboardBookSection class="pt-10"/>
  </div>
</div>
</template>
