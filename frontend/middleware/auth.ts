/**
 * Auth middleware: redirects unauthenticated users to landing page.
 */
export default defineNuxtRouteMiddleware((_to) => {
  if (import.meta.server) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    return navigateTo('/')
  }
})
