import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const username = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const accessTokenExpiresAt = ref<number | null>(null)

  const login = async (email: string, password: string): Promise<{messageTitle: string, message: string}> => {
    const response = await useUserLogin(email, password)

    username.value = response.username
    isAuthenticated.value = true
    accessTokenExpiresAt.value = response.accessTokenExpiresAt

    return {messageTitle: response.messageTitle, message: response.message}
  }

  const signup = async (username: string, email: string, password: string): Promise<{messageTitle: string, message: string}> => {
    const response = await useUserSignup(username, email, password)

    return {messageTitle: response.messageTitle, message: response.message}
  }

  const logout = async () => {
    const response = await useUserLogout()

    username.value = null
    isAuthenticated.value = false

    return {messageTitle: response.messageTitle, message: response.message}
  }

  return { username, isAuthenticated, accessTokenExpiresAt, login, signup, logout }
})