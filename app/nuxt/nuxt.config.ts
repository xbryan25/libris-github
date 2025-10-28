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
  runtimeConfig: {
    public: {
      supabaseUrl: process.env.SUPABASE_URL,
      supabaseAnonKey: process.env.SUPABASE_ANON_KEY,
    }
  },
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  modules: [
    '@nuxt/devtools',
    '@nuxt/icon',
    '@nuxt/eslint',
    '@nuxt/ui',
    '@nuxtjs/color-mode',
    '@nuxt/image'
  ],
  devServer: {
    host: '127.0.0.1',
    port: 3000,
  },
  icon: {
    mode: 'css',
    cssLayer: 'base',
    customCollections: [
      {
        prefix: 'icons',
        dir: './app/assets/icons/',
      },
    ],
  }
})