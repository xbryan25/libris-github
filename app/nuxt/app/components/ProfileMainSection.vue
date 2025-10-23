<script>
import TrustScoreDetails from './TrustScoreDetails.vue'
</script>

<template>
  <UCard class="w-[1500px] h-[250px] bg-surface border-base flex items-stretch px-10">
    <div class="flex items-center justify-start space-x-6 flex-grow">
      <Icon name="icons:exchange" class="w-35 h-35 rounded-full" />

      <div class="flex flex-col justify-center">
        <div class="text-[42px] font-bold text-base">xbryan25</div>
        <div class="text-[35px] font-bold text-base">Bryan C. Adams</div>
        <div class="text-[25px] font-bold text-muted">Joined since August 1, 2025</div>
      </div>

      <div class="flex items-center h-full">
        <USeparator orientation="vertical" class="h-[200px] border-base ml-130" type="solid" />
      </div>

      <div class="flex flex-col">
        <div class="flex items-center space-x-2">
          <div class="text-[42px] font-extrabold text-base">Trust Score</div>
          <TrustScoreDetails />
        </div>

        <div class="flex items-center space-x-3">
          <div class="text-[40px] font-semibold text-base">400</div>
          <UBadge class="bg-[#FACC15] text-white text-center px-3 py-1" variant="solid">
            Decent
          </UBadge>
        </div>

        <div class="text-[15px] font-semibold text-muted">19% more than other people</div>
      </div>
    </div>
  </UCard>
</template>
