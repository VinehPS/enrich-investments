<template>
  <div>
    <NuxtLayout name="app">
      <div class="space-y-8">
        <h1 class="text-3xl font-bold text-white">Meu Perfil</h1>

        <!-- User Info Card -->
        <div class="bg-brand-surface/50 border border-brand-border rounded-2xl p-6 lg:p-8">
          <div class="flex items-center gap-5 mb-8">
            <img
              v-if="authStore.user?.picture"
              :src="authStore.user.picture"
              :alt="authStore.user.name"
              class="w-20 h-20 rounded-2xl object-cover shadow-lg border-2 border-brand/30"
              referrerpolicy="no-referrer"
            />
            <div v-else class="w-20 h-20 rounded-2xl bg-brand/20 flex items-center justify-center">
              <span class="text-brand text-3xl font-bold">{{ authStore.user?.name?.charAt(0) }}</span>
            </div>
            <div>
              <h2 class="text-xl font-bold text-white">{{ authStore.user?.name }}</h2>
              <p class="text-gray-400 text-sm">{{ authStore.user?.email }}</p>
              <p v-if="authStore.user?.nickname" class="text-brand-light text-sm font-medium mt-0.5">@{{ authStore.user.nickname }}</p>
            </div>
          </div>

          <!-- API Key Management -->
          <div class="border-t border-brand-border pt-6">
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-brand-light" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
              Chave de API (LLM)
            </h3>

            <div v-if="authStore.user?.has_gemini_key" class="bg-green-500/10 border border-green-500/20 rounded-xl p-4 mb-4 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-green-500/20 text-green-400 rounded-lg flex items-center justify-center">✓</div>
                <div>
                  <p class="text-sm text-green-300 font-medium">API Key cadastrada</p>
                  <p class="text-xs text-gray-500">Sua chave está encriptada e segura no banco de dados.</p>
                </div>
              </div>
              <div class="flex gap-2">
                <button
                  class="text-xs bg-white/5 border border-brand-border text-gray-300 px-3 py-1.5 rounded-lg hover:bg-white/10 transition-colors"
                  @click="showUpdateKey = true"
                >
                  Atualizar
                </button>
                <button
                  :disabled="removingKey"
                  class="text-xs bg-red-500/10 border border-red-500/20 text-red-400 px-3 py-1.5 rounded-lg hover:bg-red-500/20 transition-colors"
                  @click="removeApiKey"
                >
                  {{ removingKey ? 'Removendo...' : 'Remover' }}
                </button>
              </div>
            </div>

            <div v-else class="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 mb-4">
              <p class="text-sm text-amber-200"><strong>⚠️ Nenhuma API Key cadastrada.</strong> Você precisa dela para realizar processamentos.</p>
            </div>

            <!-- Add/Update Key Form -->
            <div v-if="!authStore.user?.has_gemini_key || showUpdateKey">
              <div class="space-y-3">
                <input
                  v-model="newApiKey"
                  type="password"
                  class="w-full bg-white/5 border border-brand-border rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-brand focus:ring-1 focus:ring-brand outline-none transition-colors"
                  placeholder="Cole sua API Key aqui (AIza...)"
                />
                <div class="bg-blue-500/10 border border-blue-500/20 rounded-xl p-3 text-xs text-blue-200">
                  🔒 Sua chave será encriptada com criptografia Fernet. Recomendamos configurar limites de gastos no Google AI Studio.
                  <strong>Não nos responsabilizamos por chaves vazadas externamente.</strong>
                </div>
                <div class="flex gap-3">
                  <button
                    v-if="showUpdateKey"
                    class="border border-brand-border text-gray-300 font-medium px-6 py-2.5 rounded-xl hover:bg-white/5 transition-colors"
                    @click="showUpdateKey = false"
                  >
                    Cancelar
                  </button>
                  <button
                    :disabled="!newApiKey.trim() || savingKey"
                    class="bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold px-6 py-2.5 rounded-xl hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    @click="saveKey"
                  >
                    {{ savingKey ? 'Salvando...' : 'Salvar Chave' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Success/Error Messages -->
        <div v-if="message" :class="messageType === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-300' : 'bg-red-500/10 border-red-500/30 text-red-300'" class="border rounded-xl p-4 text-sm">
          {{ message }}
        </div>
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({ middleware: 'auth' })
useHead({ title: 'Meu Perfil — Enrich Investments' })

const authStore = useAuthStore()
const newApiKey = ref('')
const showUpdateKey = ref(false)
const savingKey = ref(false)
const removingKey = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const showMessage = (text: string, type: 'success' | 'error') => {
  message.value = text
  messageType.value = type
  setTimeout(() => { message.value = '' }, 5000)
}

const saveKey = async () => {
  savingKey.value = true
  try {
    await authStore.saveApiKey(newApiKey.value.trim())
    newApiKey.value = ''
    showUpdateKey.value = false
    showMessage('API Key salva com sucesso!', 'success')
  } catch (error: any) {
    showMessage(error.message || 'Falha ao salvar a chave.', 'error')
  } finally {
    savingKey.value = false
  }
}

const removeApiKey = async () => {
  removingKey.value = true
  try {
    await authStore.deleteApiKey()
    showMessage('API Key removida com sucesso.', 'success')
  } catch (error: any) {
    showMessage(error.message || 'Falha ao remover a chave.', 'error')
  } finally {
    removingKey.value = false
  }
}
</script>
