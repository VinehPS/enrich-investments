import { defineStore } from 'pinia'

interface UserInfo {
  email: string
  name: string
  picture: string | null
  has_gemini_key: boolean
  nickname?: string | null
}

interface AuthState {
  accessToken: string | null
  user: UserInfo | null
  isAuthenticated: boolean
  loading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: null,
    user: null,
    isAuthenticated: false,
    loading: true
  }),

  actions: {
    async loginWithGoogle(googleToken: string) {
      const api = useApi()
      try {
        const data = await api.post<{
          access_token: string
          token_type: string
          user_info: UserInfo
        }>('/auth/login', { token: googleToken })

        this.accessToken = data.access_token
        this.user = data.user_info
        this.isAuthenticated = true

        if (import.meta.client) {
          localStorage.setItem('access_token', data.access_token)
        }

        return data
      } catch (error: unknown) {
        this.clearAuth()
        throw error
      }
    },

    async fetchCurrentUser() {
      const api = useApi()
      try {
        this.loading = true
        const data = await api.get<UserInfo>('/auth/me')
        this.user = data
        this.isAuthenticated = true
      } catch {
        this.clearAuth()
      } finally {
        this.loading = false
      }
    },

    async logout() {
      const api = useApi()
      try {
        await api.post('/auth/logout')
      } catch {
        // Ignore errors on logout
      } finally {
        this.clearAuth()
      }
    },

    async deleteAccount() {
      const api = useApi()
      await api.del('/auth/me')
      this.clearAuth()
    },

    async saveApiKey(apiKey: string) {
      const api = useApi()
      await api.post('/auth/gemini-key', { gemini_key: apiKey })
      if (this.user) {
        this.user.has_gemini_key = true
      }
    },

    async deleteApiKey() {
      const api = useApi()
      await api.del('/auth/api-key')
      if (this.user) {
        this.user.has_gemini_key = false
      }
    },

    async saveNickname(nickname: string) {
      const api = useApi()
      const data = await api.post<{ nickname: string }>('/user/nickname', { nickname })
      if (this.user) {
        this.user.nickname = data.nickname
      }
      return data
    },

    initAuth() {
      if (import.meta.client) {
        const token = localStorage.getItem('access_token')
        if (token) {
          this.accessToken = token
          this.fetchCurrentUser()
        } else {
          this.loading = false
        }
      } else {
        this.loading = false
      }
    },

    clearAuth() {
      this.accessToken = null
      this.user = null
      this.isAuthenticated = false
      if (import.meta.client) {
        localStorage.removeItem('access_token')
      }
    }
  }
})

function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseUrl as string

  const getToken = (): string | null => {
    if (import.meta.client) {
      return localStorage.getItem('access_token')
    }
    return null
  }

  const request = async <T = unknown>(
    endpoint: string,
    options: { method?: string; body?: unknown; params?: Record<string, string> } = {}
  ): Promise<T> => {
    const { method = 'GET', body, params } = options
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`

    const url = new URL(`${baseURL}${endpoint}`)
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) url.searchParams.append(key, params[key])
      })
    }

    const res = await fetch(url.toString(), {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(err.detail || 'Request failed')
    }

    if (res.status === 204) return undefined as T
    return await res.json()
  }

  return {
    get: <T = unknown>(endpoint: string, params?: Record<string, string>) => request<T>(endpoint, { method: 'GET', params }),
    post: <T = unknown>(endpoint: string, body?: unknown) => request<T>(endpoint, { method: 'POST', body }),
    patch: <T = unknown>(endpoint: string, body?: unknown) => request<T>(endpoint, { method: 'PATCH', body }),
    put: <T = unknown>(endpoint: string, body?: unknown) => request<T>(endpoint, { method: 'PUT', body }),
    del: <T = unknown>(endpoint: string) => request<T>(endpoint, { method: 'DELETE' })
  }
}
