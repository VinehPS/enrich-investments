/**
 * Auth initialization plugin: restores auth state from localStorage on app start.
 */
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  authStore.initAuth()
})
