/**
 * Composable for making authenticated API calls to the FastAPI backend.
 */
export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseUrl as string

  const getToken = (): string | null => {
    if (import.meta.client) {
      return localStorage.getItem('access_token')
    }
    return null
  }

  const request = async <T = any>(
    endpoint: string,
    options: {
      method?: string
      body?: any
      params?: Record<string, string>
      auth?: boolean
    } = {}
  ): Promise<T> => {
    const { method = 'GET', body, params, auth = true } = options

    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    }

    if (auth) {
      const token = getToken()
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }

    const url = new URL(`${baseURL}${endpoint}`)
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
          url.searchParams.append(key, params[key])
        }
      })
    }

    const res = await fetch(url.toString(), {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined
    })

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }))
      throw new ApiError(res.status, errorData.detail || 'Request failed')
    }

    if (res.status === 204) {
      return undefined as T
    }

    return await res.json()
  }

  return {
    get: <T = any>(endpoint: string, params?: Record<string, string>) =>
      request<T>(endpoint, { method: 'GET', params }),

    post: <T = any>(endpoint: string, body?: any) =>
      request<T>(endpoint, { method: 'POST', body }),

    patch: <T = any>(endpoint: string, body?: any) =>
      request<T>(endpoint, { method: 'PATCH', body }),

    put: <T = any>(endpoint: string, body?: any) =>
      request<T>(endpoint, { method: 'PUT', body }),

    del: <T = any>(endpoint: string) =>
      request<T>(endpoint, { method: 'DELETE' })
  }
}

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
    this.name = 'ApiError'
  }
}
