<template>
  <div>
    <NuxtLayout name="app">
      <div class="space-y-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-white">Minhas Perguntas</h1>
            <p class="text-gray-400 mt-1">Gerencie suas perguntas personalizadas para as análises.</p>
          </div>
        </div>

        <!-- Info Alert -->
        <div class="bg-blue-500/10 border border-blue-500/20 rounded-xl p-4 text-sm text-blue-200">
          <strong>ℹ️ Dica:</strong> Cada pergunta deve ter no máximo 500 caracteres. A resposta esperada pelo motor de IA é sempre "Sim" ou "Não", seguida de uma justificativa.
        </div>

        <!-- Add Question Form -->
        <div class="bg-brand-surface/50 border border-brand-border rounded-2xl p-6">
          <h3 class="text-lg font-semibold text-white mb-4">Nova Pergunta</h3>
          <div class="space-y-3">
            <textarea
              v-model="newQuestionText"
              rows="3"
              maxlength="500"
              class="w-full bg-white/5 border border-brand-border rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-brand focus:ring-1 focus:ring-brand outline-none transition-colors resize-none"
              placeholder="Ex: A empresa possui margens operacionais estáveis nos últimos 3 anos?"
            ></textarea>
            <div class="flex items-center justify-between">
              <div class="flex gap-3">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input v-model="newQuestionType" type="radio" value="stocks" class="accent-yellow-500" />
                  <span class="text-sm text-gray-300">Ações</span>
                </label>
                <label class="flex items-center gap-2 cursor-pointer">
                  <input v-model="newQuestionType" type="radio" value="real_estate_funds" class="accent-yellow-500" />
                  <span class="text-sm text-gray-300">FIIs</span>
                </label>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-xs text-gray-500">{{ newQuestionText.length }}/500</span>
                <button
                  :disabled="!newQuestionText.trim() || !newQuestionType || addingQuestion"
                  class="bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold px-6 py-2.5 rounded-xl hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  @click="addQuestion"
                >
                  {{ addingQuestion ? 'Adicionando...' : 'Adicionar' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Questions List -->
        <div class="space-y-3">
          <!-- Filter Tabs -->
          <div class="flex gap-2 mb-4">
            <button
              :class="filterType === '' ? 'bg-brand/20 text-brand-light border-brand/40' : 'bg-white/5 text-gray-400 border-brand-border'"
              class="border px-4 py-1.5 rounded-lg text-sm font-medium transition-colors"
              @click="filterType = ''"
            >
              Todas
            </button>
            <button
              :class="filterType === 'stocks' ? 'bg-blue-500/20 text-blue-400 border-blue-500/40' : 'bg-white/5 text-gray-400 border-brand-border'"
              class="border px-4 py-1.5 rounded-lg text-sm font-medium transition-colors"
              @click="filterType = 'stocks'"
            >
              Ações
            </button>
            <button
              :class="filterType === 'real_estate_funds' ? 'bg-purple-500/20 text-purple-400 border-purple-500/40' : 'bg-white/5 text-gray-400 border-brand-border'"
              class="border px-4 py-1.5 rounded-lg text-sm font-medium transition-colors"
              @click="filterType = 'real_estate_funds'"
            >
              Fundos
            </button>
          </div>

          <div v-if="questionsStore.loading" class="text-center py-12 text-gray-500">Carregando perguntas...</div>

          <div v-else-if="filteredQuestions.length === 0" class="text-center py-12">
            <p class="text-gray-500">Nenhuma pergunta cadastrada ainda.</p>
          </div>

          <div
            v-for="q in filteredQuestions"
            v-else
            :key="q.id"
            class="bg-brand-surface/50 border border-brand-border rounded-xl p-4 group hover:border-brand/30 transition-colors"
          >
            <div v-if="editingId !== q.id" class="flex items-start justify-between gap-4">
              <div class="flex-1">
                <p class="text-sm text-gray-200">{{ q.text }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <span
                    :class="q.type === 'stocks' ? 'bg-blue-500/20 text-blue-400' : 'bg-purple-500/20 text-purple-400'"
                    class="text-xs font-medium px-2 py-0.5 rounded-full"
                  >
                    {{ q.type === 'stocks' ? 'Ação' : 'FII' }}
                  </span>
                  <span class="text-xs text-gray-600">{{ new Date(q.created_at).toLocaleDateString('pt-BR') }}</span>
                </div>
              </div>
              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button class="text-gray-500 hover:text-brand-light p-1.5 rounded-lg hover:bg-white/5 transition-colors" @click="startEdit(q)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                </button>
                <button class="text-gray-500 hover:text-red-400 p-1.5 rounded-lg hover:bg-white/5 transition-colors" @click="deleteQuestion(q.id)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-else class="space-y-3">
              <textarea
                v-model="editText"
                rows="2"
                maxlength="500"
                class="w-full bg-white/5 border border-brand rounded-xl px-4 py-3 text-white focus:ring-1 focus:ring-brand outline-none resize-none"
              ></textarea>
              <div class="flex justify-end gap-2">
                <button class="text-sm text-gray-400 px-4 py-1.5 rounded-lg hover:bg-white/5 transition-colors" @click="cancelEdit">Cancelar</button>
                <button
                  :disabled="!editText.trim()"
                  class="text-sm bg-brand text-brand-bg font-semibold px-4 py-1.5 rounded-lg hover:brightness-110 transition-all disabled:opacity-50"
                  @click="saveEdit"
                >
                  Salvar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useQuestionsStore } from '~/stores/questions'

definePageMeta({ middleware: 'auth' })
useHead({ title: 'Minhas Perguntas — Enrich Investments' })

const questionsStore = useQuestionsStore()

const newQuestionText = ref('')
const newQuestionType = ref('stocks')
const addingQuestion = ref(false)
const filterType = ref('')

const editingId = ref<string | null>(null)
const editText = ref('')

onMounted(() => {
  questionsStore.fetchUserQuestions()
})

const filteredQuestions = computed(() => {
  if (!filterType.value) return questionsStore.userQuestions
  return questionsStore.userQuestions.filter(q => q.type === filterType.value)
})

const addQuestion = async () => {
  addingQuestion.value = true
  try {
    await questionsStore.createQuestion(newQuestionText.value.trim(), newQuestionType.value)
    newQuestionText.value = ''
  } catch (error: any) {
    alert(error.message || 'Falha ao criar pergunta.')
  } finally {
    addingQuestion.value = false
  }
}

const startEdit = (q: { id: string; text: string }) => {
  editingId.value = q.id
  editText.value = q.text
}

const cancelEdit = () => {
  editingId.value = null
  editText.value = ''
}

const saveEdit = async () => {
  if (!editingId.value) return
  try {
    await questionsStore.updateQuestion(editingId.value, editText.value.trim())
    cancelEdit()
  } catch (error: any) {
    alert(error.message || 'Falha ao atualizar pergunta.')
  }
}

const deleteQuestion = async (id: string) => {
  if (!confirm('Tem certeza que deseja excluir esta pergunta?')) return
  try {
    await questionsStore.deleteQuestion(id)
  } catch (error: any) {
    alert(error.message || 'Falha ao excluir pergunta.')
  }
}
</script>
