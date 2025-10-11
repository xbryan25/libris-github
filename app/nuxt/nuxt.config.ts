import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  modules: [
    '@nuxt/devtools',
    '@nuxt/icon',
    '@nuxt/eslint',
    '@nuxt/ui'
  ],
  devServer: {
    host: '127.0.0.1',
    port: 3000,
  },
  icon: {
    mode: 'css',
    cssLayer: 'base'
  }
})