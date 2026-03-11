import { defineStore } from 'pinia'
import { useApi } from '~/composables/useApi'

export interface ProcessingResult {
  id: string
  ticker: string
  type: string
  questions_answers: { question: string; answer: string; justification: string }[]
  processing_date: string
  nickname?: string
}

interface HistoryState {
  myHistory: ProcessingResult[]
  globalHistory: ProcessingResult[]
  loading: boolean
  globalLoading: boolean
}

export const useHistoryStore = defineStore('history', {
  state: (): HistoryState => ({
    myHistory: [],
    globalHistory: [],
    loading: false,
    globalLoading: false
  }),

  actions: {
    async fetchMyHistory(params?: { ticker?: string; type?: string; start_date?: string }) {
      const api = useApi()
      this.loading = true
      try {
        const queryParams: Record<string, string> = {}
        if (params?.ticker) queryParams.ticker = params.ticker
        if (params?.type) queryParams.type = params.type
        if (params?.start_date) queryParams.start_date = params.start_date

        const data = await api.get<ProcessingResult[]>('/analyze/history', queryParams)
        this.myHistory = data
      } catch (error) {
        console.error('Failed to fetch history:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchGlobalHistory(params?: { ticker?: string; type?: string; search?: string; sort?: string }) {
      const api = useApi()
      this.globalLoading = true
      try {
        const queryParams: Record<string, string> = {}
        if (params?.ticker) queryParams.ticker = params.ticker
        if (params?.type) queryParams.type = params.type
        if (params?.search) queryParams.search = params.search
        if (params?.sort) queryParams.sort = params.sort

        const data = await api.get<ProcessingResult[]>('/analyze/history/global', queryParams)
        this.globalHistory = data
      } catch (error) {
        console.error('Failed to fetch global history:', error)
      } finally {
        this.globalLoading = false
      }
    },

    async analyzeAsset(ticker: string, type: string, questions?: { text: string }[]) {
      const api = useApi()
      const body: Record<string, unknown> = { ticker, type }
      if (questions && questions.length > 0) {
        body.questions = questions
      }
      return await api.post<ProcessingResult>('/analyze', body)
    }
  }
})
