<script setup lang="ts">
import { h, resolveComponent } from 'vue';
import type { TableColumn } from '@nuxt/ui';

const UCheckbox = resolveComponent('UCheckbox');

const data = ref([
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings' xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: true,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationID: '123',
    notificationDate: 'Mar 11',
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
      return h(
        resolveComponent('NuxtLink'),
        { to: `/notifications/${row.original.notificationID}`, class: 'flex gap-10 no-underline' },
        () => [
          h('p', { class: 'font-bold' }, row.original.notificationHeader),
          h('p', { class: 'text-sm text-gray-500 truncate' }, row.original.notificationBody),
        ],
      );
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
    cell: ({ row }) => {
      return h(
        resolveComponent('NuxtLink'),
        { to: `/notifications/${row.original.notificationID}`, class: 'flex gap-10 no-underline' },
        () => [h('p', { class: 'font-bold' }, row.original.notificationDate)],
      );
    },
    meta: {
      class: {
        th: 'w-20',
        td: 'w-20',
      },
    },
  },
];

const table = useTemplateRef('table');

const sortItems = ref(['Show Newest First', 'Show Oldest First']);
const sortValue = ref('Show Newest First');

const showItems = ref(['Show All', 'Show Only Read', 'Show Only Unread']);
const showValue = ref('Show All');

const selectAllNotifsInPageValue = ref(false);
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
      <div class="flex w-full">
        <div class="flex-1 flex gap-3 items-center pl-3">
          <UCheckbox
            v-model="selectAllNotifsInPageValue"
            size="xl"
            :ui="{ base: 'cursor-pointer' }"
          />

          <UTooltip v-if="selectAllNotifsInPageValue" text="Delete">
            <UButton icon="material-symbols:delete-outline" class="cursor-pointer" />
          </UTooltip>

          <UTooltip v-if="selectAllNotifsInPageValue" text="Mark as read">
            <UButton icon="material-symbols:mark-email-read" class="cursor-pointer" />
          </UTooltip>
        </div>

        <div class="flex-1 flex justify-end gap-3">
          <USelect v-model="showValue" :items="showItems" class="min-w-45" />
          <USelect v-model="sortValue" :items="sortItems" class="min-w-45" />
        </div>
      </div>

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

      <UPagination show-edges :sibling-count="2" :total="10" class="pt-5" />
    </div>
  </div>
</template>
