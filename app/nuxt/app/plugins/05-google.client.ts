import { defineNuxtPlugin } from '#app'

import googleLoginPlugin from 'vue3-google-login'


export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(googleLoginPlugin, {
    clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID
  })
})