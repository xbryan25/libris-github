export {};

declare module '#app' {
  interface NuxtApp {
    $apiFetch: typeof $fetch;
  }
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $apiFetch: typeof $fetch;
  }
}
