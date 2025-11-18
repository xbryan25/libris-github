<script setup lang="ts">
import { h, resolveComponent } from 'vue';
import type { TableColumn } from '@nuxt/ui';

const UCheckbox = resolveComponent('UCheckbox');

const data = ref([
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings' xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: true,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
]);

const columns: TableColumn[] = [
  {
    id: 'select',
    cell: () =>
      h(UCheckbox, {
        icon: 'tabler:check',
        ui: {
          base: 'cursor-pointer',
        },
      }),
    meta: {
      class: {
        th: 'w-12',
        td: 'w-12',
      },
    },
  },
  {
    id: 'notification',
    cell: ({ row }) => {
      return h('div', { class: 'flex gap-10' }, [
        h('p', { class: 'font-bold' }, row.original.notificationHeader),
        h('p', { class: 'text-sm text-gray-500 truncate' }, row.original.notificationBody),
      ]);
    },
    meta: {
      class: {
        th: 'max-w-20',
        td: 'max-w-20',
      },
    },
  },
  {
    id: 'date',
    cell: 'Mar 11',
    meta: {
      class: {
        th: 'w-20',
        td: 'w-20',
      },
    },
  },
];

const table = useTemplateRef('table');

const items = ref(['All', 'Read', 'Unread']);
const value = ref('All');
</script>

<template>
  <div class="flex flex-col w-full pt-10 px-20 gap-5">
    <div class="flex-1 flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <Icon name="material-symbols:notifications-rounded" class="w-8 h-8 text-base" />
        <h1 class="font-bold text-3xl">Notifications</h1>
      </div>

      <p class="text-muted">Check your latest notifications and important actions.</p>
    </div>

    <div class="flex-1 flex flex-col items-center px-20">
      <!-- <div class="flex w-full">
        <div class="flex items-center justify-center gap-2">
          <UCheckbox size="xl" />
          <USelect v-model="value" :items="items" />
        </div>

        <UButton>Delete</UButton>
        <UButton>Mark as Read</UButton>
      </div> -->

      <UTable
        ref="table"
        loading
        :data="data"
        :columns="columns"
        class="table-auto !w-full !min-w-0 cursor-pointer"
        :ui="{ root: 'table-auto !w-full !min-w-0' }"
        :meta="{
          class: {
            // The conditional function must be nested here
            tr: (row) => (row.original.hasRead ? '' : 'bg-surface'),
          },
        }"
      />

      <UPagination show-edges :sibling-count="0" :total="10" class="pt-5" />
    </div>
  </div>
</template>
