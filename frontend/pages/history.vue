<template>
  <div>
    <NuxtLayout name="app">
      <div class="space-y-8">
        <div>
          <h1 class="text-3xl font-bold text-white">Meu Histórico</h1>
          <p class="text-gray-400 mt-1">Todos os seus processamentos anteriores.</p>
        </div>

        <!-- Filters -->
        <div class="flex flex-wrap gap-3">
          <input
            v-model="filterTicker"
            type="text"
            class="bg-white/5 border border-brand-border rounded-xl px-4 py-2 text-white placeholder-gray-500 focus:border-brand outline-none text-sm w-48"
            placeholder="Filtrar por código..."
          />
          <select
            v-model="filterType"
            class="bg-white/5 border border-brand-border rounded-xl px-4 py-2 text-white focus:border-brand outline-none text-sm appearance-none"
          >
            <option value="">Todos os tipos</option>
            <option value="stocks">Ações</option>
            <option value="real_estate_funds">Fundos</option>
          </select>
          <button
            :disabled="historyStore.loading"
            class="bg-brand/20 text-brand-light font-medium px-4 py-2 rounded-xl hover:bg-brand/30 transition-colors text-sm flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            @click="loadHistory"
          >
            <template v-if="historyStore.loading">
              <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              <span>Filtrando...</span>
            </template>
            <template v-else>
              <span>Filtrar</span>
            </template>
          </button>
        </div>

        <!-- Loading -->
        <div v-if="historyStore.loading" class="text-center py-12 text-gray-500">
          <svg class="animate-spin w-8 h-8 mx-auto mb-2 text-brand" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          Carregando histórico...
        </div>

        <!-- Empty state -->
        <div v-else-if="historyStore.myHistory.length === 0" class="text-center py-16">
          <svg class="w-16 h-16 mx-auto text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <p class="text-gray-500 text-lg">Nenhum processamento realizado ainda.</p>
          <NuxtLink to="/dashboard" class="inline-block mt-4 text-brand-light hover:text-brand underline font-medium">Fazer primeiro processamento →</NuxtLink>
        </div>

        <!-- Results Cards -->
        <div v-else class="space-y-4">
          <div
            v-for="result in historyStore.myHistory"
            :key="result.id"
            class="bg-brand-surface/50 border border-brand-border rounded-2xl p-6 hover:border-brand/20 transition-colors"
          >
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <span
                  :class="result.type === 'stocks' ? 'bg-blue-500/20 text-blue-400' : 'bg-purple-500/20 text-purple-400'"
                  class="text-xs font-bold px-3 py-1 rounded-full"
                >
                  {{ result.type === 'stocks' ? 'Ação' : 'FII' }}
                </span>
                <h3 class="text-lg font-bold text-white">{{ result.ticker }}</h3>
              </div>
              <span class="text-xs text-gray-500">{{ new Date(result.processing_date).toLocaleString('pt-BR') }}</span>
            </div>

            <div class="grid gap-2">
              <div
                v-for="(qa, idx) in result.questions_answers"
                :key="idx"
                class="bg-white/5 rounded-xl p-3 flex items-start gap-3"
              >
                <span
                  :class="qa.answer?.toLowerCase() === 'sim' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'"
                  class="text-xs font-bold px-2 py-0.5 rounded-full flex-shrink-0 mt-0.5"
                >
                  {{ qa.answer }}
                </span>
                <div>
                  <p class="text-sm text-gray-300">{{ qa.question }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ qa.justification }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useHistoryStore } from '~/stores/history'

definePageMeta({ middleware: 'auth' })
useHead({ title: 'Meu Histórico — Enrich Investments' })

const historyStore = useHistoryStore()
const filterTicker = ref('')
const filterType = ref('')

onMounted(() => {
  loadHistory()
})

const loadHistory = () => {
  historyStore.fetchMyHistory({
    ticker: filterTicker.value,
    type: filterType.value
  })
}
</script>
