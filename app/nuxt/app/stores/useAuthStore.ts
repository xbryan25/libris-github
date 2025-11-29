import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user_id = ref<string | null>(null)
  const username = ref<string | null>(null)
  const isAuthenticated = ref(false)

  const login = async (email: string, password: string): Promise<{messageTitle: string, message: string}> => {
    const response = await useUserLogin(email, password)

    user_id.value = response.user_id
    username.value = response.username
    isAuthenticated.value = true

    return {messageTitle: response.messageTitle, message: response.message}
  }

  const signup = async (username: string, email: string, password: string): Promise<{messageTitle: string, message: string, userId: string}> => {
    const response = await useUserSignup(username, email, password)

    return {messageTitle: response.messageTitle, message: response.message, userId: response.userId}
  }

  const logout = async () => {
    const response = await useUserLogout()
   
    user_id.value = null
    username.value = null
    isAuthenticated.value = false

    return {messageTitle: response.messageTitle, message: response.message}
  }

  return { user_id, username, isAuthenticated, login, signup, logout }
})