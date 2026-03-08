import { defineStore } from 'pinia'

interface QuestionItem {
  id: string
  text: string
  type: string
  created_at: string
}

interface DefaultQuestions {
  stocks: { text: string }[]
  real_estate_funds: { text: string }[]
}

interface QuestionsState {
  userQuestions: QuestionItem[]
  defaultQuestions: DefaultQuestions
  loading: boolean
  defaultLoaded: boolean
}

export const useQuestionsStore = defineStore('questions', {
  state: (): QuestionsState => ({
    userQuestions: [],
    defaultQuestions: { stocks: [], real_estate_funds: [] },
    loading: false,
    defaultLoaded: false
  }),

  actions: {
    async fetchDefaultQuestions() {
      if (this.defaultLoaded) return
      const api = useApi()
      try {
        const data = await api.get<DefaultQuestions>('/analyze/default-questions')
        this.defaultQuestions = data
        this.defaultLoaded = true
      } catch (error) {
        console.error('Failed to load default questions:', error)
      }
    },

    async fetchUserQuestions(type?: string) {
      const api = useApi()
      this.loading = true
      try {
        const params: Record<string, string> = {}
        if (type) params.type = type
        const data = await api.get<QuestionItem[]>('/questions', params)
        this.userQuestions = data
      } catch (error) {
        console.error('Failed to load user questions:', error)
      } finally {
        this.loading = false
      }
    },

    async createQuestion(text: string, type: string) {
      const api = useApi()
      const data = await api.post<QuestionItem>('/questions', { text, type })
      this.userQuestions.push(data)
      return data
    },

    async updateQuestion(id: string, text: string) {
      const api = useApi()
      const data = await api.patch<QuestionItem>(`/questions/${id}`, { text })
      const idx = this.userQuestions.findIndex(q => q.id === id)
      if (idx !== -1) this.userQuestions[idx] = data
      return data
    },

    async deleteQuestion(id: string) {
      const api = useApi()
      await api.del(`/questions/${id}`)
      this.userQuestions = this.userQuestions.filter(q => q.id !== id)
    }
  }
})
