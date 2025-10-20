<script setup lang="ts"></script>

<template>
  <div class="w-full h-[400px] text-white flex flex-col items-center justify-center">
    <div class="flex-[2] w-full rounded-t-xl overflow-hidden">
      <NuxtImg src="/images/authImage1.jpg" class="w-full h-full object-cover" alt="Auth image" />
    </div>

    <div
      class="flex-1 flex flex-col gap-[10px] px-5 py-4 bg-surface-hover text-white w-full rounded-b-xl"
    >
      <div class="flex-1 flex flex-col gap-1 items-center pb-1">
        <UTooltip text="The Passion WithinThe Passion WithinThe Passion Within">
          <p class="text-lg text-left font-semibold text-base truncate w-full">
            The Passion WithinThe Passion Within
          </p>
        </UTooltip>

        <UTooltip text="by Sam Huertas" class="flex-[3]">
          <p class="text-left text-xs text-base truncate">by Sam Huertas</p>
        </UTooltip>

        <USeparator color="primary" type="solid" class="flex-1" />

        <UTooltip text="samalexis" class="flex-[3]">
          <p class="text-left text-xs text-base truncate w-full">Owned by: samalexis</p>
        </UTooltip>
      </div>

      <div class="flex gap-2 items-start">
        <UBadge class="font-bold rounded-full">For rent</UBadge>
        <UBadge color="error" class="font-bold rounded-full">For sale</UBadge>
      </div>

      <div class="flex flex-col gap-1">
        <div class="flex gap-2 items-center">
          <div class="flex-1 flex gap-1 items-center">
            <Icon name="solar:clock-circle-bold" class="w-5 h-5 text-base" />
            <p class="flex-1 text-sm font-semibold text-base">Rent</p>
          </div>

          <div class="flex items-center">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent" />
            <p class="text-xs text-primary font-semibold">4/day</p>
          </div>
        </div>

        <div class="flex gap-2 items-center">
          <div class="flex-1 flex gap-1 items-center">
            <Icon name="solar:cart-large-2-bold-duotone" class="w-5 h-5 text-base" />
            <p class="flex-1 text-sm font-semibold text-base">Buy</p>
          </div>

          <div class="flex items-center">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent" />
            <p class="text-xs text-primary font-semibold">50</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
