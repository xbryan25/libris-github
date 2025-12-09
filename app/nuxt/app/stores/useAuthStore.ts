import { defineStore } from 'pinia'
import { ref } from 'vue'

import { googleAuthCodeLogin } from 'vue3-google-login';

export const useAuthStore = defineStore('auth', () => {
  const userId = ref<string | null>(null)
  const username = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const isEmailVerified = ref(false)
  const isGoogleLogin = ref(false)

  const login = async (email: string, password: string): Promise<{messageTitle: string, message: string, isEmailVerified: boolean}> => {
    try {
      const response = await useUserLogin(email, password);

      userId.value = response.userId;
      username.value = response.username;
      isAuthenticated.value = true;
      isEmailVerified.value = response.isEmailVerified
      isGoogleLogin.value = false;

      return {
        messageTitle: response.messageTitle,
        message: response.message,
        isEmailVerified: response.isEmailVerified
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

      userId.value = response.userId;
      username.value = response.username;
      isAuthenticated.value = true;
      isEmailVerified.value = response.isEmailVerified
      isGoogleLogin.value = true;

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

  const signup = async (username: string, email: string, password: string): Promise<{userId: string, messageTitle: string, message: string}> => {
    const response = await useUserSignup(username, email, password)

    return {userId: response.userId, messageTitle: response.messageTitle, message: response.message}
  }

  const logout = async () => {
    const response = await useUserLogout()
   
    userId.value = null
    username.value = null
    isAuthenticated.value = false

    return {messageTitle: response.messageTitle, message: response.message}
  }

  return { userId, username, isAuthenticated, isEmailVerified, isGoogleLogin, login, googleLogin, signup, logout }
})