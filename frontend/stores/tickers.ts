import { defineStore } from 'pinia'
import { useApi } from '~/composables/useApi'

interface Ticker {
  ticker: string
  name: string
}

interface TickersState {
  stocks: Ticker[]
  fiis: Ticker[]
  loading: boolean
  loaded: boolean
}

export const useTickersStore = defineStore('tickers', {
  state: (): TickersState => ({
    stocks: [],
    fiis: [],
    loading: false,
    loaded: false
  }),

  getters: {
    allTickers(state): Ticker[] {
      return [...state.stocks, ...state.fiis]
    }
  },

  actions: {
    async fetchTickers() {
      if (this.loaded) return

      const api = useApi()
      this.loading = true
      try {
        const data = await api.get<{
          stocks: Ticker[]
          fiis: Ticker[]
          last_updated: string
          cached: boolean
        }>('/tickers/available')

        this.stocks = data.stocks
        this.fiis = data.fiis
        this.loaded = true
      } catch (error) {
        console.error('Failed to fetch tickers:', error)
      } finally {
        this.loading = false
      }
    }
  }
})
