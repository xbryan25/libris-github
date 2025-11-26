import { defineStore } from 'pinia'
import { ref } from 'vue'

import { googleAuthCodeLogin } from 'vue3-google-login';

export const useAuthStore = defineStore('auth', () => {
  const userId = ref<string | null>(null)
  const username = ref<string | null>(null)
  const isAuthenticated = ref(false)

  const login = async (
    email: string,
    password: string
  ): Promise<{ messageTitle: string; message: string }> => {
    try {
      console.log('before response?')
      const response = await useUserLogin(email, password);
      console.log(response)

      userId.value = response.user_id;
      username.value = response.username;
      isAuthenticated.value = true;

      return {
        messageTitle: response.messageTitle,
        message: response.message,
      };
    } catch (error: any) {
      console.error('Login failed in store:', error);

      // rethrow error so the component’s try/catch can handle it
      throw error;
    }
  }

  const googleLogin = async (
  ): Promise<{ messageTitle: string; message: string }> => {
    try {
      const googlePopupResponse = await googleAuthCodeLogin(); // may trigger COOP warning

      console.log(googlePopupResponse)

      const code = googlePopupResponse.code;

      const response = await useUserGoogleLogin(code);

      userId.value = response.user_id;
      username.value = response.username;
      isAuthenticated.value = true;

      return {
        messageTitle: response.messageTitle,
        message: response.message,
      };
    } catch (error: any) {
      console.error('Login failed in store:', error);

      // rethrow error so the component’s try/catch can handle it
      throw error;
    }
  }

  const signup = async (username: string, email: string, password: string): Promise<{messageTitle: string, message: string}> => {
    const response = await useUserSignup(username, email, password)

    return {messageTitle: response.messageTitle, message: response.message}
  }

  const logout = async () => {
    const response = await useUserLogout()
   
    userId.value = null
    username.value = null
    isAuthenticated.value = false

    return {messageTitle: response.messageTitle, message: response.message}
  }

  return { userId, username, isAuthenticated, login, googleLogin, signup, logout }
})