<template>
  <div>
    <NuxtLayout name="app">
      <div class="space-y-8">
        <div>
          <h1 class="text-3xl font-bold text-white">Histórico Global</h1>
          <p class="text-gray-400 mt-1">Veja as análises realizadas por toda a comunidade de investidores.</p>
        </div>

        <!-- Filters Row -->
        <div class="flex flex-wrap gap-3 items-center">
          <input
            v-model="searchQuery"
            type="text"
            class="bg-white/5 border border-brand-border rounded-xl px-4 py-2 text-white placeholder-gray-500 focus:border-brand outline-none text-sm flex-1 min-w-[200px]"
            placeholder="Buscar por código ou pergunta..."
            @keyup.enter="loadGlobalHistory"
          />
          <div class="flex gap-2">
            <button
              @click="filterType = ''; loadGlobalHistory()"
              :class="filterType === '' ? 'bg-brand/20 text-brand-light border-brand/40' : 'bg-white/5 text-gray-400 border-brand-border'"
              class="border px-4 py-2 rounded-xl text-sm font-medium transition-colors"
            >
              Todos
            </button>
            <button
              @click="filterType = 'stocks'; loadGlobalHistory()"
              :class="filterType === 'stocks' ? 'bg-blue-500/20 text-blue-400 border-blue-500/40' : 'bg-white/5 text-gray-400 border-brand-border'"
              class="border px-4 py-2 rounded-xl text-sm font-medium transition-colors"
            >
              Ações
            </button>
            <button
              @click="filterType = 'real_estate_funds'; loadGlobalHistory()"
              :class="filterType === 'real_estate_funds' ? 'bg-purple-500/20 text-purple-400 border-purple-500/40' : 'bg-white/5 text-gray-400 border-brand-border'"
              class="border px-4 py-2 rounded-xl text-sm font-medium transition-colors"
            >
              Fundos
            </button>
          </div>
          <select
            v-model="sortOrder"
            @change="loadGlobalHistory"
            class="bg-white/5 border border-brand-border rounded-xl px-4 py-2 text-white focus:border-brand outline-none text-sm appearance-none"
          >
            <option value="newest">Mais recentes</option>
            <option value="oldest">Mais antigos</option>
          </select>
        </div>

        <!-- Loading -->
        <div v-if="historyStore.globalLoading" class="text-center py-12 text-gray-500">
          <svg class="animate-spin w-8 h-8 mx-auto mb-2 text-brand" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          Carregando histórico global...
        </div>

        <!-- Empty state -->
        <div v-else-if="historyStore.globalHistory.length === 0" class="text-center py-16">
          <svg class="w-16 h-16 mx-auto text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <p class="text-gray-500 text-lg">Nenhum processamento encontrado na comunidade.</p>
        </div>

        <!-- Results -->
        <div v-else class="space-y-4">
          <div
            v-for="result in historyStore.globalHistory"
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
              <div class="text-right">
                <p class="text-xs text-gray-500">{{ new Date(result.processing_date).toLocaleString('pt-BR') }}</p>
                <p v-if="result.nickname" class="text-xs text-brand-light font-medium">por @{{ result.nickname }}</p>
              </div>
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
useHead({ title: 'Histórico Global — Enrich Investments' })

const historyStore = useHistoryStore()
const searchQuery = ref('')
const filterType = ref('')
const sortOrder = ref('newest')

onMounted(() => {
  loadGlobalHistory()
})

const loadGlobalHistory = () => {
  historyStore.fetchGlobalHistory({
    search: searchQuery.value,
    type: filterType.value,
    sort: sortOrder.value
  })
}
</script>
