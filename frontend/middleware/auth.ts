/**
 * Auth middleware: redirects unauthenticated users to landing page.
 */
export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    return navigateTo('/')
  }
})
