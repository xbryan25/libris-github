<template>
    <UPopover>
      <UButton icon="i-heroicons-information-circle" variant="ghost" size="lg" />
      <template #content>
        <div class="p-3 text-sm text-muted w-[300px] space-y-3">
          <div class="font-semibold mb-2">Trust Score Criteria</div>
  
          <div class="flex flex-col space-y-2">
            <div class="flex items-center justify-between">
              <span>1000 - 951</span>
              <UBadge class="bg-[#15803D] text-white text-center px-3" variant="solid">Perfect</UBadge>
            </div>
            <div class="flex items-center justify-between">
              <span>950 - 751</span>
              <UBadge class="bg-[#22C55E] text-white text-center px-3" variant="solid">Exceptional</UBadge>
            </div>
            <div class="flex items-center justify-between">
              <span>750 - 500</span>
              <UBadge class="bg-[#84CC16] text-white text-center px-3" variant="solid">Good</UBadge>
            </div>
            <div class="flex items-center justify-between">
              <span>500 - 251</span>
              <UBadge class="bg-[#FACC15] text-white text-center px-3" variant="solid">Decent</UBadge>
            </div>
            <div class="flex items-center justify-between">
              <span>250 - 51</span>
              <UBadge class="bg-[#CA8A04] text-white text-center px-3" variant="solid">Bad</UBadge>
            </div>
            <div class="flex items-center justify-between">
              <span>50 - 0</span>
              <UBadge class="bg-[#000000] text-white text-center px-3" variant="solid">Poor</UBadge>
            </div>
          </div>
        </div>
      </template>
    </UPopover>
  </template>
  