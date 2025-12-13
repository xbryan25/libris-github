<script setup lang="ts">
const props = defineProps<{
  isOpenViewMeetupLocationOnMap: boolean;
  latitude: number;
  longitude: number;
}>();

const emit = defineEmits<{
  (e: 'update:openViewMeetupLocationOnMap', value: boolean): void;
}>();

const isOpenViewMeetupLocationOnMap = computed({
  get: () => props.isOpenViewMeetupLocationOnMap,
  set: (val: boolean) => {
    emit('update:openViewMeetupLocationOnMap', val);
  },
});
</script>

<template>
  <UModal v-model:open="isOpenViewMeetupLocationOnMap" :ui="{ content: 'max-w-[90vw]' }">
    <template #content>
      <div class="flex">
        <LMap
          ref="map"
          :zoom="17"
          :center="[props.latitude, props.longitude]"
          :use-global-leaflet="false"
          style="height: 90vh"
        >
          <LTileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            layer-type="base"
            name="OpenStreetMap"
          />

          <LMarker
            v-if="latitude !== null && longitude !== null"
            :lat-lng="[props.latitude, props.longitude]"
          />
        </LMap>
      </div>
    </template>
  </UModal>
</template>
