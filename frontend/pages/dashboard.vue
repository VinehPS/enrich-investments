<template>
  <div>
    <NuxtLayout name="app">
      <div class="space-y-8">
        <!-- Page Header -->
        <div>
          <h1 class="text-3xl font-bold text-white">Dashboard</h1>
          <p class="text-gray-400 mt-1">Selecione um ativo e inicie uma nova análise inteligente.</p>
        </div>

        <!-- Analysis Form Card -->
        <div class="bg-brand-surface/50 border border-brand-border rounded-2xl p-6 lg:p-8">
          <!-- Ticker Search -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-2">Código do Ativo</label>
            <div ref="dropdownRef" class="relative">
              <input
                v-model="searchQuery"
                type="text"
                class="w-full bg-white/5 border border-brand-border rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-brand focus:ring-1 focus:ring-brand outline-none transition-colors"
                placeholder="Buscar por código (ex: BBAS3, HGLG11)..."
                @focus="showDropdown = true"
                @input="handleSearch"
              />
              <!-- Dropdown -->
              <Transition name="fade">
                <div
                  v-if="showDropdown && filteredTickers.length > 0"
                  class="absolute z-20 w-full mt-1 bg-brand-surface border border-brand-border rounded-xl shadow-2xl max-h-60 overflow-y-auto"
                >
                  <button
                    v-for="t in filteredTickers"
                    :key="t.ticker"
                    class="w-full text-left px-4 py-3 hover:bg-white/5 transition-colors flex items-center justify-between border-b border-brand-border last:border-0"
                    @click="selectTicker(t)"
                  >
                    <div>
                      <span class="text-white font-semibold">{{ t.ticker }}</span>
                      <span class="text-gray-500 text-sm ml-2">{{ t.name }}</span>
                    </div>
                    <span
                      :class="isStock(t.ticker) ? 'bg-blue-500/20 text-blue-400' : 'bg-purple-500/20 text-purple-400'"
                      class="text-xs font-medium px-2 py-0.5 rounded-full"
                    >
                      {{ isStock(t.ticker) ? 'Ação' : 'FII' }}
                    </span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- Selected ticker display -->
            <div v-if="selectedTicker" class="mt-2 flex items-center gap-2">
              <span class="text-brand-light font-semibold">{{ selectedTicker.ticker }}</span>
              <span class="text-gray-500 text-sm">- {{ selectedTicker.name }}</span>
              <button class="text-gray-500 hover:text-red-400 ml-2 transition-colors" @click="clearTicker">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
          </div>

          <!-- Questions Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-3">Selecione as Perguntas</label>
            <div class="flex gap-4 mb-4">
              <label class="flex items-center gap-2 cursor-pointer group">
                <input
                  v-model="questionMode"
                  type="radio"
                  value="default"
                  class="w-4 h-4 text-brand focus:ring-brand accent-yellow-500"
                />
                <span class="text-sm text-gray-300 group-hover:text-white transition-colors">Perguntas Padrão</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer group">
                <input
                  v-model="questionMode"
                  type="radio"
                  value="custom"
                  class="w-4 h-4 text-brand focus:ring-brand accent-yellow-500"
                />
                <span class="text-sm text-gray-300 group-hover:text-white transition-colors">Minhas Perguntas</span>
              </label>
            </div>

            <!-- Default Questions Preview -->
            <div v-if="questionMode === 'default'" class="bg-white/5 rounded-xl p-4 space-y-2">
              <p class="text-xs text-gray-500 mb-2 uppercase tracking-wider font-medium">Perguntas que serão utilizadas:</p>
              <div v-if="selectedType === 'stocks' || !selectedType">
                <p class="text-xs text-brand-light font-semibold mb-1">Ações:</p>
                <div v-for="q in questionsStore.defaultQuestions.stocks" :key="q.text" class="text-sm text-gray-300 flex items-start gap-2 py-1">
                  <span class="text-brand mt-0.5">•</span>
                  {{ q.text }}
                </div>
              </div>
              <div v-if="selectedType === 'real_estate_funds' || !selectedType" class="mt-3">
                <p class="text-xs text-brand-light font-semibold mb-1">Fundos Imobiliários:</p>
                <div v-for="q in questionsStore.defaultQuestions.real_estate_funds" :key="q.text" class="text-sm text-gray-300 flex items-start gap-2 py-1">
                  <span class="text-brand mt-0.5">•</span>
                  {{ q.text }}
                </div>
              </div>
            </div>

            <!-- Custom Questions -->
            <div v-if="questionMode === 'custom'">
              <div v-if="questionsStore.userQuestions.length === 0" class="bg-blue-500/10 border border-blue-500/20 rounded-xl p-4 text-sm text-blue-200">
                <strong>ℹ️ Sem perguntas cadastradas ainda.</strong> Cada pergunta deve ter no máximo 500 caracteres e a resposta esperada deve ser "Sim" ou "Não".
                <NuxtLink to="/questions" class="underline font-semibold hover:text-blue-100 ml-1">Criar perguntas →</NuxtLink>
              </div>
              <div v-else class="bg-white/5 rounded-xl p-4 space-y-2">
                <div v-for="q in questionsStore.userQuestions" :key="q.id" class="flex items-center gap-3">
                  <input v-model="selectedCustomQuestions" type="checkbox" :value="q.id" class="w-4 h-4 accent-yellow-500 rounded" />
                  <span class="text-sm text-gray-300">{{ q.text }}</span>
                  <span class="text-xs text-gray-600">({{ q.type === 'stocks' ? 'Ação' : 'FII' }})</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Process Button -->
          <button
            :disabled="!canProcess || processing"
            class="w-full bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold py-4 rounded-xl hover:brightness-110 transition-all duration-200 shadow-lg shadow-brand/30 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg"
            @click="startProcessing"
          >
            <template v-if="processing">
              <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Processando análise...
            </template>
            <template v-else>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              Iniciar Processamento
            </template>
          </button>
        </div>

        <!-- Latest Result -->
        <Transition name="fade">
          <div v-if="latestResult" class="bg-brand-surface/50 border border-green-500/30 rounded-2xl p-6 lg:p-8">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 bg-green-500/20 text-green-400 rounded-xl flex items-center justify-center text-lg font-bold">✓</div>
              <div>
                <h2 class="text-xl font-bold text-white">{{ latestResult.ticker }} — Análise Completa</h2>
                <p class="text-xs text-gray-500">{{ new Date(latestResult.processing_date).toLocaleString('pt-BR') }}</p>
              </div>
            </div>
            <div class="space-y-3">
              <div
                v-for="(qa, idx) in latestResult.questions_answers"
                :key="idx"
                class="bg-white/5 rounded-xl p-4"
              >
                <p class="text-sm text-gray-300 mb-2">{{ qa.question }}</p>
                <div class="flex items-start gap-3">
                  <span
                    :class="qa.answer?.toLowerCase() === 'sim' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'"
                    class="text-xs font-bold px-3 py-1 rounded-full flex-shrink-0"
                  >
                    {{ qa.answer }}
                  </span>
                  <p class="text-xs text-gray-500 leading-relaxed">{{ qa.justification }}</p>
                </div>
              </div>
            </div>
          </div>
        </Transition>

        <!-- Processing Error -->
        <div v-if="processError" class="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-sm text-red-300">
          <strong>Erro:</strong> {{ processError }}
        </div>
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useTickersStore } from '~/stores/tickers'
import { useQuestionsStore } from '~/stores/questions'
import { useHistoryStore, type ProcessingResult } from '~/stores/history'

definePageMeta({
  middleware: 'auth'
})

useHead({ title: 'Dashboard — Enrich Investments' })

const authStore = useAuthStore()
const tickersStore = useTickersStore()
const questionsStore = useQuestionsStore()
const historyStore = useHistoryStore()

const searchQuery = ref('')
const showDropdown = ref(false)
const selectedTicker = ref<{ ticker: string; name: string } | null>(null)
const selectedType = ref<string>('')
const questionMode = ref<'default' | 'custom'>('default')
const selectedCustomQuestions = ref<string[]>([])
const processing = ref(false)
const processError = ref('')
const latestResult = ref<ProcessingResult | null>(null)
const dropdownRef = ref<HTMLElement | null>(null)

// Load data on mount
onMounted(async () => {
  await tickersStore.fetchTickers()
  await questionsStore.fetchDefaultQuestions()
  await questionsStore.fetchUserQuestions()

  // Close dropdown on outside click
  document.addEventListener('click', (e: MouseEvent) => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target as HTMLElement)) {
      showDropdown.value = false
    }
  })
})

const filteredTickers = computed(() => {
  if (!searchQuery.value.trim()) return tickersStore.allTickers.slice(0, 20)
  const q = searchQuery.value.toLowerCase()
  return tickersStore.allTickers
    .filter(t => t.ticker.toLowerCase().includes(q) || t.name.toLowerCase().includes(q))
    .slice(0, 20)
})

const isStock = (ticker: string) => {
  return tickersStore.stocks.some(s => s.ticker === ticker)
}

const selectTicker = (t: { ticker: string; name: string }) => {
  selectedTicker.value = t
  searchQuery.value = t.ticker
  showDropdown.value = false
  selectedType.value = isStock(t.ticker) ? 'stocks' : 'real_estate_funds'
}

const clearTicker = () => {
  selectedTicker.value = null
  searchQuery.value = ''
  selectedType.value = ''
}

const handleSearch = () => {
  showDropdown.value = true
  if (selectedTicker.value && searchQuery.value !== selectedTicker.value.ticker) {
    selectedTicker.value = null
    selectedType.value = ''
  }
}

const canProcess = computed(() => {
  return selectedTicker.value && authStore.user?.has_gemini_key
})

const startProcessing = async () => {
  if (!selectedTicker.value || !selectedType.value) return

  processing.value = true
  processError.value = ''
  latestResult.value = null

  try {
    let questions: { text: string }[] | undefined
    if (questionMode.value === 'custom' && selectedCustomQuestions.value.length > 0) {
      questions = questionsStore.userQuestions
        .filter(q => selectedCustomQuestions.value.includes(q.id))
        .map(q => ({ text: q.text }))
    }

    const result = await historyStore.analyzeAsset(
      selectedTicker.value.ticker,
      selectedType.value,
      questions
    )
    latestResult.value = result
  } catch (error: unknown) {
    processError.value = (error as Error).message || 'Falha no processamento.'
  } finally {
    processing.value = false
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}
</style>
