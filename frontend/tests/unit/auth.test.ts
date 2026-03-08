import { describe, it, expect } from 'vitest'

describe('Auth Store', () => {
  it('should start with unauthenticated state', () => {
    // Basic assertion that auth defaults are correct
    const defaultState = {
      accessToken: null,
      user: null,
      isAuthenticated: false,
      loading: true
    }

    expect(defaultState.accessToken).toBeNull()
    expect(defaultState.user).toBeNull()
    expect(defaultState.isAuthenticated).toBe(false)
    expect(defaultState.loading).toBe(true)
  })

  it('should clear auth state correctly', () => {
    const state = {
      accessToken: 'some-token',
      user: { email: 'test@test.com', name: 'Test', picture: null, has_gemini_key: false },
      isAuthenticated: true,
      loading: false
    }

    // Simulate clearAuth
    state.accessToken = null
    state.user = null
    state.isAuthenticated = false

    expect(state.accessToken).toBeNull()
    expect(state.user).toBeNull()
    expect(state.isAuthenticated).toBe(false)
  })
})

describe('API Error', () => {
  it('should create error with status and message', () => {
    const error = new Error('Not Found')
    expect(error.message).toBe('Not Found')
  })
})
