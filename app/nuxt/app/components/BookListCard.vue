<script setup lang="ts">
import type { Book } from '~/types';

const props = defineProps<{
  cardType: string;
  bookDetails?: Book | null;
}>();
</script>

<template>
  <NuxtLink
    v-if="props.cardType === 'hasContent'"
    :to="`/books/${props.bookDetails?.bookId}`"
    class="w-full h-[400px] flex flex-col items-center justify-center transition-transform duration-300 hover:scale-103 cursor-pointer"
  >
    <div class="flex-[2] w-full rounded-t-xl overflow-hidden">
      <NuxtImg
        v-if="props.bookDetails?.firstImageUrl"
        :src="props.bookDetails?.firstImageUrl"
        class="w-full h-full object-cover"
        alt="Auth image"
      />
      <NuxtImg
        v-else
        src="/images/noImageImage.jpg"
        class="w-full h-full object-cover"
        alt="Auth image"
      />
    </div>

    <div class="flex-1 flex flex-col gap-[10px] px-5 py-4 bg-surface-hover w-full rounded-b-xl">
      <div class="flex-1 flex flex-col gap-1 items-center pb-1">
        <UTooltip :text="props.bookDetails?.title">
          <p class="text-lg text-center font-semibold text-base truncate w-full">
            {{ props.bookDetails?.title }}
          </p>
        </UTooltip>

        <UTooltip :text="props.bookDetails?.author" class="flex-[3]">
          <p class="text-left text-xs text-base truncate">by {{ props.bookDetails?.author }}</p>
        </UTooltip>

        <USeparator color="primary" type="solid" class="flex-1" />

        <UTooltip :text="props.bookDetails?.ownerUsername" class="flex-[3]">
          <p class="text-left text-xs text-base truncate w-full">
            Owned by: {{ props.bookDetails?.ownerUsername }}
          </p>
        </UTooltip>
      </div>

      <div class="flex gap-2 items-start">
        <UBadge
          v-if="
            ['rent', 'both'].includes(
              props.bookDetails?.availability ? props.bookDetails?.availability : '',
            )
          "
          class="font-bold rounded-full"
          >For Rent</UBadge
        >
        <UBadge
          v-if="
            ['purchase', 'both'].includes(
              props.bookDetails?.availability ? props.bookDetails?.availability : '',
            )
          "
          color="error"
          class="font-bold rounded-full"
          >For Sale</UBadge
        >
      </div>

      <div class="flex flex-col gap-1">
        <div
          v-if="
            ['rent', 'both'].includes(
              props.bookDetails?.availability ? props.bookDetails?.availability : '',
            )
          "
          class="flex gap-2 items-center"
        >
          <div class="flex-1 flex gap-1 items-center">
            <Icon name="solar:clock-circle-bold" class="w-5 h-5 text-base" />
            <p class="flex-1 text-sm font-semibold text-base">Rent</p>
          </div>

          <div class="flex items-center">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent" />
            <p class="text-xs text-primary font-semibold">
              {{ props.bookDetails?.dailyRentPrice }}/day
            </p>
          </div>
        </div>

        <div
          v-if="
            ['purchase', 'both'].includes(
              props.bookDetails?.availability ? props.bookDetails?.availability : '',
            )
          "
          class="flex gap-2 items-center"
        >
          <div class="flex-1 flex gap-1 items-center">
            <Icon name="solar:cart-large-2-bold-duotone" class="w-5 h-5 text-base" />
            <p class="flex-1 text-sm font-semibold text-base">Buy</p>
          </div>

          <div class="flex items-center">
            <Icon name="fluent:book-coins-20-regular" class="w-5 h-5 text-accent" />
            <p class="text-xs text-primary font-semibold">
              {{ props.bookDetails?.purchasePrice }}
            </p>
          </div>
        </div>

        <div
          v-if="
            ['rent', 'purchase'].includes(
              props.bookDetails?.availability ? props.bookDetails?.availability : '',
            )
          "
          class="flex gap-2 items-center h-5"
        ></div>
      </div>
    </div>
  </NuxtLink>

  <div v-else class="w-full h-[400px] flex flex-col items-center justify-center bg-transparent" />
</template>
