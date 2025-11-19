<script setup lang="ts">
import { h, resolveComponent } from 'vue';
import type { TableColumn } from '@nuxt/ui';

import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});

const UCheckbox = resolveComponent('UCheckbox');

type Notification = {
  notificationId: string;
  notificationDate: string;
  notificationHeader: string;
  notificationBody: string;
  hasRead: boolean;
};

const data = ref<Notification[]>([
  {
    notificationId: '123',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings' xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: true,
  },
  {
    notificationId: '1234',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '1235',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '1236',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '1237',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '1238',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '1239',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '12324',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '12344',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '12355',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '12366',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
  {
    notificationId: '12377',
    notificationDate: 'Mar 11',
    notificationHeader: 'Return Request Approved',
    notificationBody:
      "xbryan25 has successfully requested to return the book which is titled 'The Way Of Kings'",
    hasRead: false,
  },
]);

const selectedRows = ref<Set<string>>(new Set());

const columns: TableColumn<Notification>[] = [
  {
    id: 'select',
    cell: ({ row }) =>
      h(UCheckbox, {
        ui: {
          base: 'cursor-pointer',
        },
        modelValue: computed(() => selectedRows.value.has(row.original.notificationId)).value,
        'onUpdate:modelValue': (value: boolean) => {
          console.log(value);
          toggleRow(row.original.notificationId, value);
        },
        'aria-label': 'Select row',
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
        { to: `/notifications/${row.original.notificationId}`, class: 'flex gap-10 no-underline' },
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
        { to: `/notifications/${row.original.notificationId}`, class: 'flex gap-10 no-underline' },
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

const externalCheckboxValue = computed<boolean | 'indeterminate'>(() => {
  if (selectedRows.value.size === 0) return false;
  if (selectedRows.value.size === data.value.length) return true;
  return 'indeterminate';
});

// Handler for external checkbox
function toggleAll(value: boolean | 'indeterminate') {
  const val = value === 'indeterminate' ? true : value;
  if (val) selectedRows.value = new Set(data.value.map((r) => r.notificationId));
  else selectedRows.value = new Set();
}

// Row checkbox toggle
function toggleRow(id: string, value: boolean) {
  const newSet = new Set(selectedRows.value);
  if (value) newSet.add(id);
  else newSet.delete(id);
  selectedRows.value = newSet;
}

const sortItems = ref(['Show Newest First', 'Show Oldest First']);
const sortValue = ref('Show Newest First');

const showItems = ref(['Show All', 'Show Only Read', 'Show Only Unread']);
const showValue = ref('Show All');
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
        <div class="flex-1 flex gap-3 items-center pl-[15px]">
          <UCheckbox
            :model-value="externalCheckboxValue"
            :ui="{ base: 'cursor-pointer' }"
            @update:model-value="toggleAll"
          />

          <UTooltip v-if="externalCheckboxValue" text="Delete">
            <UButton
              icon="material-symbols:delete-outline"
              color="neutral"
              class="cursor-pointer"
            />
          </UTooltip>

          <UTooltip v-if="externalCheckboxValue" text="Mark as read">
            <UButton
              icon="material-symbols:mark-email-read"
              color="neutral"
              class="cursor-pointer"
            />
          </UTooltip>
        </div>

        <div class="flex-1 flex justify-end gap-3">
          <USelect v-model="showValue" :items="showItems" class="min-w-45" />
          <USelect v-model="sortValue" :items="sortItems" class="min-w-45" />
        </div>
      </div>

      <UTable
        ref="table"
        :data="data"
        :columns="columns"
        class="table-auto !w-full !min-w-0"
        :ui="{ root: 'table-auto !w-full !min-w-0' }"
        :meta="{
          class: {
            tr: (row) =>
              row.original.hasRead
                ? 'cursor-pointer hover:outline hover:outline-1 hover:outline-surface'
                : 'cursor-pointer hover:outline hover:outline-1 hover:outline-surface bg-surface ',
          },
        }"
      />

      <UPagination show-edges :sibling-count="2" :total="10" class="pt-5" />
    </div>
  </div>
</template>
