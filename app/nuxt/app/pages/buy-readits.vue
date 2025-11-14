<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div class="h-screen w-full overflow-hidden bg-background text-base">
    <div class="w-full flex flex-col items-center gap-10 mt-10">
      <div class="flex w-full max-w-[1364px]">
        <NuxtLink :to="`/browse`" class="flex gap-2 cursor-pointer">
          <Icon name="material-symbols:arrow-back-rounded" class="w-5 h-5" />
          <span>Back to Browse</span>
        </NuxtLink>
      </div>

      <div class="flex justify-center max-w-[1364px] w-full">
        <UCard class="w-full">
          <div class="flex items-center">
            <div class="flex-1 flex flex-col gap-2">
              <h2 class="font-semibold text-lg">Current Balance</h2>
              <h1 class="font-bold text-4xl">1000 Readits</h1>
              <p>Each book requires Readits to rent/buy.</p>
            </div>

            <Icon name="fluent:book-coins-20-regular" class="w-25 h-25 text-accent" />
          </div>
        </UCard>
      </div>

      <div class="flex-1 flex flex-col items-center justify-center gap-5">
        <div class="flex gap-5">
          <UPricingPlan
            title="Starter Pack"
            description="Perfect for casual readers who want a small boost of credits."
            price="₱150"
            discount="₱100"
            billing-cycle="/one-time"
            :button="{
              label: 'Buy now',
            }"
            orientation="horizontal"
            variant="outline"
            class="max-w-2xl max-h-60"
            :ui="{
              features: '!flex !mt-6 w-full',
              button:
                'cursor-pointer bg-inverted hover:bg-inverted hover:opacity-80 active:bg-inverted active:opacity-80',
            }"
          >
            <template #features
              ><div class="flex items-center w-full py-2 gap-1">
                <Icon
                  name="fluent:book-coins-20-regular"
                  class="w-10 h-10 text-accent relative -left-2"
                />

                <span class="text-2xl font-semibold text-accent relative -left-2">200 readits</span>
              </div></template
            >
          </UPricingPlan>

          <UPricingPlan
            title="Popular Pack"
            description="Great for regular readers who enjoy renting books more often."
            :badge="{
              label: 'Most popular',
              variant: 'solid',
            }"
            price="₱200"
            discount="₱150"
            billing-cycle="/one-time"
            :button="{
              label: 'Buy now',
            }"
            orientation="horizontal"
            variant="outline"
            class="max-w-2xl max-h-60 border-3 border-blue-500"
            :ui="{
              features: '!flex !mt-6 w-full',
              button: 'cursor-pointer bg-blue-500 hover:bg-blue-400 active:bg-blue-400',
              badge: 'bg-blue-500',
            }"
          >
            <template #features
              ><div class="flex items-center w-full py-2 gap-1">
                <Icon
                  name="fluent:book-coins-20-regular"
                  class="w-10 h-10 text-accent relative -left-2"
                />

                <span class="text-2xl font-semibold text-accent relative -left-2">600 readits</span>
              </div></template
            >
          </UPricingPlan>
        </div>

        <div class="flex gap-5">
          <UPricingPlan
            title="Pro Pack"
            description="Ideal for committed book lovers who read week after week."
            price="₱400"
            discount="₱350"
            billing-cycle="/one-time"
            :button="{
              label: 'Buy now',
            }"
            orientation="horizontal"
            variant="outline"
            class="max-w-2xl max-h-60"
            :ui="{
              features: '!flex !mt-6 w-full',
              button:
                'cursor-pointer bg-inverted hover:bg-inverted hover:opacity-80 active:bg-inverted active:opacity-80',
            }"
          >
            <template #features
              ><div class="flex items-center w-full py-2 gap-1">
                <Icon
                  name="fluent:book-coins-20-regular"
                  class="w-10 h-10 text-accent relative -left-2"
                />

                <span class="text-2xl font-semibold text-accent relative -left-2"
                  >1000 readits</span
                >
              </div>
            </template>
          </UPricingPlan>
          <UPricingPlan
            title="Ultra Pack"
            description="Designed for power readers who never want to run out of Readits."
            :badge="{
              label: 'Best value',
              variant: 'solid',
            }"
            price="₱850"
            discount="₱750"
            billing-cycle="/one-time"
            :button="{
              label: 'Buy now',
            }"
            orientation="horizontal"
            variant="outline"
            class="max-w-2xl max-h-60 border-3 border-orange-500"
            :ui="{
              features: '!flex !mt-6 w-full',
              button: 'cursor-pointer bg-orange-500 hover:bg-orange-400 active:bg-orange-400',
              badge: 'bg-orange-500',
            }"
          >
            <template #features
              ><div class="flex items-center w-full py-2 gap-1">
                <Icon
                  name="fluent:book-coins-20-regular"
                  class="w-10 h-10 text-accent relative -left-2"
                />

                <span class="text-2xl font-semibold text-accent relative -left-2"
                  >5000 readits</span
                >
              </div></template
            >
          </UPricingPlan>
        </div>
      </div>
    </div>
  </div>
</template>
