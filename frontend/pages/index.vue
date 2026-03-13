<template>
  <div class="min-h-screen bg-brand-bg overflow-hidden">
    <!-- ===== HERO SECTION ===== -->
    <section class="relative">
      <!-- Background decoration -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -right-40 w-[600px] h-[600px] bg-brand/5 rounded-full blur-3xl"></div>
        <div class="absolute top-60 -left-40 w-[400px] h-[400px] bg-brand-dark/10 rounded-full blur-3xl"></div>
      </div>

      <!-- Top bar -->
      <nav class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-brand to-brand-light rounded-xl flex items-center justify-center shadow-lg shadow-brand/30">
            <span class="text-brand-bg font-bold text-xl">E</span>
          </div>
          <span class="text-2xl font-bold text-white">Enrich<span class="text-brand-light">Investments</span></span>
        </div>

        <!-- Login CTA Desktop -->
        <button
          :disabled="googleLoginLoading"
          class="hidden sm:flex items-center gap-2 bg-white text-gray-800 font-semibold px-5 py-2.5 rounded-xl hover:bg-gray-100 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed"
          @click="handleGoogleLogin"
        >
          <template v-if="googleLoginLoading">
            <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Entrando...
          </template>
          <template v-else>
            <svg class="w-5 h-5" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
            Entrar com Google
          </template>
        </button>
      </nav>

      <!-- Hero Content -->
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-20 lg:pt-20 lg:pb-32">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <div class="inline-flex items-center gap-2 bg-brand/10 border border-brand/20 text-brand-light text-sm font-medium px-4 py-1.5 rounded-full mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/></svg>
              Potencializado por Inteligência Artificial
            </div>
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-white leading-tight mb-6">
              Enriqueça suas
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand to-brand-light"> análises de investimentos</span>
            </h1>
            <p class="text-lg text-gray-400 leading-relaxed mb-8 max-w-lg">
              Utilize o poder do <strong class="text-gray-200">Google Gemini</strong> para preencher automaticamente seu
              <strong class="text-gray-200">Diagrama do Cerrado</strong> e o
              <strong class="text-gray-200">Diagrama de Fundos Imobiliários</strong>, economizando horas de pesquisa manual.
            </p>
            <div class="flex flex-col sm:flex-row gap-4">
              <button
                :disabled="googleLoginLoading"
                class="flex items-center justify-center gap-3 bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold px-8 py-4 rounded-xl hover:brightness-110 transition-all duration-200 shadow-lg shadow-brand/30 hover:shadow-brand/50 hover:-translate-y-0.5 text-lg disabled:opacity-60 disabled:cursor-not-allowed"
                @click="handleGoogleLogin"
              >
                <template v-if="googleLoginLoading">
                  <svg class="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  <span>Conectando...</span>
                </template>
                <template v-else>
                  <svg class="w-6 h-6" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="currentColor" opacity="0.7"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="currentColor" opacity="0.8"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="currentColor" opacity="0.6"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="currentColor" opacity="0.9"/></svg>
                  <span>Começar Agora — É Grátis</span>
                </template>
              </button>
              <a
                href="#como-funciona"
                class="flex items-center justify-center gap-2 border border-brand-border text-gray-300 font-semibold px-8 py-4 rounded-xl hover:bg-white/5 hover:border-gray-500 transition-all duration-200"
              >
                Como Funciona
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/></svg>
              </a>
            </div>
          </div>

          <!-- Hero Visual: Example Output Card -->
          <div class="hidden lg:block">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-brand/20 to-brand-dark/20 blur-3xl rounded-full"></div>
              <div class="relative bg-brand-surface/80 backdrop-blur-xl border border-brand-border rounded-2xl p-6 shadow-2xl">
                <div class="flex items-center gap-3 mb-4">
                  <div class="w-8 h-8 bg-green-500/20 text-green-400 rounded-lg flex items-center justify-center text-sm font-bold">✓</div>
                  <div>
                    <h3 class="text-white font-semibold">BBAS3 — Análise Completa</h3>
                    <p class="text-xs text-gray-500">Processado em 08/03/2026</p>
                  </div>
                </div>
                <div class="space-y-3">
                  <div v-for="item in exampleOutput" :key="item.question" class="bg-white/5 rounded-xl p-3">
                    <p class="text-sm text-gray-300 mb-1">{{ item.question }}</p>
                    <div class="flex items-center gap-2">
                      <span :class="item.answer === 'Sim' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'" class="text-xs font-bold px-2 py-0.5 rounded-full">{{ item.answer }}</span>
                      <span class="text-xs text-gray-500 truncate">{{ item.justification }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== FEATURES SECTION ===== -->
    <section id="como-funciona" class="relative py-20 lg:py-32">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Tudo que você precisa para tomar decisões
            <span class="text-brand-light">mais assertivas</span>
          </h2>
          <p class="text-gray-400 max-w-2xl mx-auto text-lg">
            Nosso sistema combina dados de mercado em tempo real com IA para responder automaticamente às perguntas do seu diagrama de investimentos.
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="feature in features" :key="feature.title" class="group bg-brand-surface/50 border border-brand-border rounded-2xl p-6 hover:bg-brand-surface hover:border-brand/30 transition-all duration-300 hover:-translate-y-1">
            <div class="w-12 h-12 bg-brand/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-brand/20 transition-colors">
              <span class="text-2xl">{{ feature.icon }}</span>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">{{ feature.title }}</h3>
            <p class="text-gray-400 text-sm leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== HOW IT WORKS ===== -->
    <section class="relative py-20 border-t border-brand-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Simples, rápido e <span class="text-brand-light">inteligente</span>
          </h2>
          <p class="text-gray-400 max-w-xl mx-auto">3 passos para transformar suas análises de investimento</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="(step, idx) in steps" :key="step.title" class="text-center relative">
            <div class="w-16 h-16 bg-gradient-to-br from-brand to-brand-dark rounded-2xl flex items-center justify-center mx-auto mb-4 text-brand-bg font-bold text-xl shadow-lg shadow-brand/20">
              {{ idx + 1 }}
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">{{ step.title }}</h3>
            <p class="text-gray-400 text-sm">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== REQUIREMENTS SECTION ===== -->
    <section class="relative py-20 border-t border-brand-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-brand-surface/50 border border-brand-border rounded-2xl p-8 lg:p-12 text-center">
          <h2 class="text-3xl font-bold text-white mb-6">O que você precisa para começar?</h2>
          <div class="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto mb-8">
            <div class="bg-white/5 rounded-xl p-5 text-left">
              <div class="flex items-center gap-3 mb-2">
                <svg class="w-8 h-8 text-brand-light" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                <h3 class="text-lg font-semibold text-white">Conta Google</h3>
              </div>
              <p class="text-gray-400 text-sm">Usamos o login do Google para garantir segurança e praticidade. É obrigatório para acessar o sistema.</p>
            </div>
            <div class="bg-white/5 rounded-xl p-5 text-left">
              <div class="flex items-center gap-3 mb-2">
                <svg class="w-8 h-8 text-brand-light" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
                <h3 class="text-lg font-semibold text-white">API Key do Gemini</h3>
              </div>
              <p class="text-gray-400 text-sm">Você precisará de uma chave de API do Google AI Studio (gratuita) para alimentar o motor de IA do sistema.</p>
            </div>
          </div>
          <button
            :disabled="googleLoginLoading"
            class="bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold px-10 py-4 rounded-xl hover:brightness-110 transition-all duration-200 shadow-lg shadow-brand/30 text-lg disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 justify-center"
            @click="handleGoogleLogin"
          >
            <template v-if="googleLoginLoading">
              <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              <span>Redirecionando para login...</span>
            </template>
            <template v-else>
              <span>Criar Minha Conta Gratuitamente</span>
            </template>
          </button>
        </div>
      </div>
    </section>

    <!-- ===== FOOTER ===== -->
    <footer class="border-t border-brand-border py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-gray-500 text-sm">
          © {{ new Date().getFullYear() }} Enrich Investments. Potencializado por Google Gemini AI.
        </p>
      </div>
    </footer>

    <!-- ===== ONBOARDING MODALS ===== -->
    <!-- Nickname Modal -->
    <Transition name="modal">
      <div v-if="showNicknameModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
        <div class="bg-brand-surface border border-brand-border rounded-2xl p-8 w-full max-w-md shadow-2xl">
          <h2 class="text-2xl font-bold text-white mb-2">Escolha seu Nickname</h2>
          <p class="text-gray-400 text-sm mb-6">
            Seu nickname será público e exibido nos históricos globais. Máximo 25 caracteres.
          </p>
          <div class="mb-4">
            <input
              v-model="nickname"
              maxlength="25"
              type="text"
              class="w-full bg-white/5 border border-brand-border rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-brand focus:ring-1 focus:ring-brand outline-none transition-colors"
              placeholder="Seu nickname..."
              @keyup.enter="submitNickname"
            />
            <div class="flex justify-between mt-1">
              <span v-if="nicknameError" class="text-red-400 text-xs">{{ nicknameError }}</span>
              <span v-else class="text-xs text-gray-500">Não toleramos nomes ofensivos, agressivos ou discriminatórios.</span>
              <span class="text-xs text-gray-500">{{ nickname.length }}/25</span>
            </div>
          </div>
          <button
            :disabled="!nickname.trim() || nicknameLoading"
            class="w-full bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold py-3 rounded-xl hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            @click="submitNickname"
          >
            <span v-if="nicknameLoading">Validando...</span>
            <span v-else>Confirmar Nickname</span>
          </button>
        </div>
      </div>
    </Transition>

    <!-- API Key Modal -->
    <Transition name="modal">
      <div v-if="showApiKeyModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
        <div class="bg-brand-surface border border-brand-border rounded-2xl p-8 w-full max-w-lg shadow-2xl">
          <h2 class="text-2xl font-bold text-white mb-2">Cadastre sua API Key</h2>
          <p class="text-gray-400 text-sm mb-4">
            Para o motor de IA funcionar, precisamos da sua chave do Google AI Studio (Gemini).
          </p>

          <!-- How to get key link -->
          <button
            class="flex items-center gap-2 text-brand-light text-sm font-medium mb-4 hover:text-brand transition-colors"
            @click="showHowToGetKey = !showHowToGetKey"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ showHowToGetKey ? 'Ocultar instruções' : 'Como conseguir minha API Key?' }}
          </button>

          <Transition name="slide">
            <div v-if="showHowToGetKey" class="bg-white/5 rounded-xl p-4 mb-4 text-sm text-gray-300 space-y-2 border border-brand-border">
              <p><strong class="text-white">1.</strong> Acesse <a href="https://aistudio.google.com/apikey" target="_blank" class="text-brand-light underline hover:text-brand">aistudio.google.com/apikey</a></p>
              <p><strong class="text-white">2.</strong> Faça login com sua conta Google</p>
              <p><strong class="text-white">3.</strong> Clique em <strong class="text-white">"Create API Key"</strong></p>
              <p><strong class="text-white">4.</strong> Copie a chave gerada e cole aqui</p>
              <div class="mt-3 bg-amber-500/10 border border-amber-500/20 rounded-lg p-3 text-amber-200 text-xs">
                <strong>⚠️ Importante:</strong> Recomendamos fortemente que você configure limites de gastos e tokens na sua chave. Isso protege contra uso excessivo acidental.
              </div>
            </div>
          </Transition>

          <div class="mb-4">
            <input
              v-model="apiKey"
              type="password"
              class="w-full bg-white/5 border border-brand-border rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-brand focus:ring-1 focus:ring-brand outline-none transition-colors"
              placeholder="AIza..."
            />
            <span v-if="apiKeyError" class="text-red-400 text-xs mt-1 block">{{ apiKeyError }}</span>
          </div>

          <!-- Security alert -->
          <div class="bg-blue-500/10 border border-blue-500/20 rounded-xl p-3 mb-4 text-xs text-blue-200">
            🔒 Sua chave será <strong>encriptada</strong> no banco de dados com criptografia simétrica (Fernet). Ninguém — nem os administradores — poderá vê-la em texto puro. Contudo, <strong>não nos responsabilizamos por chaves vazadas externamente</strong>.
          </div>

          <div class="flex gap-3">
            <button
              class="flex-1 border border-brand-border text-gray-300 font-semibold py-3 rounded-xl hover:bg-white/5 transition-colors"
              @click="skipApiKey"
            >
              Pular por Agora
            </button>
            <button
              :disabled="!apiKey.trim() || apiKeyLoading"
              class="flex-1 bg-gradient-to-r from-brand to-brand-dark text-brand-bg font-bold py-3 rounded-xl hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              @click="submitApiKey"
            >
              <span v-if="apiKeyLoading">Salvando...</span>
              <span v-else>Salvar Chave</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useModalStore } from '~/stores/modal'

definePageMeta({
  layout: 'default'
})

useHead({
  title: 'Enrich Investments — Análise de Ações e FIIs com Inteligência Artificial',
  meta: [
    { name: 'description', content: 'Plataforma de enriquecimento de dados para o Diagrama do Cerrado e Diagrama de Fundos Imobiliários. Análise automatizada de ações e FIIs usando Google Gemini AI. Tome decisões de investimento mais assertivas.' },
    { name: 'keywords', content: 'investimentos, ações, fundos imobiliários, FIIs, diagrama do cerrado, análise fundamentalista, inteligência artificial, Gemini, B3, bolsa de valores' },
    { property: 'og:title', content: 'Enrich Investments — Análise de Ações e FIIs com IA' },
    { property: 'og:description', content: 'Preencha automaticamente seu Diagrama do Cerrado e Diagrama de FIIs com Inteligência Artificial.' },
    { property: 'og:type', content: 'website' },
    { name: 'referrer', content: 'no-referrer-when-downgrade' }
  ]
})

const authStore = useAuthStore()
const modalStore = useModalStore()

// Onboarding state
const showNicknameModal = ref(false)
const showApiKeyModal = ref(false)
const showHowToGetKey = ref(false)

const nickname = ref('')
const nicknameError = ref('')
const nicknameLoading = ref(false)

const apiKey = ref('')
const apiKeyError = ref('')
const apiKeyLoading = ref(false)
const googleLoginLoading = ref(false)

// Example output data for the hero visual
const exampleOutput = [
  { question: 'A empresa apresentou lucro líquido consistente nos últimos 5 anos?', answer: 'Sim', justification: 'O Banco do Brasil manteve crescimento consistente...' },
  { question: 'O ROE está acima de 15%?', answer: 'Sim', justification: 'ROE atual de 21.3%, bem acima do threshold...' },
  { question: 'A relação Dívida Líquida / EBITDA é menor que 3.0x?', answer: 'Não', justification: 'Bancos operam com alavancagem estruturalmente...' }
]

const features = [
  { icon: '🤖', title: 'Motor de IA Avançado', description: 'Utilize o Google Gemini para buscar, interpretar e responder perguntas complexas sobre qualquer ativo listado na B3.' },
  { icon: '📊', title: 'Diagrama do Cerrado', description: 'Preencha automaticamente as perguntas do diagrama de ações da metodologia Barsi/Bazin com respostas fundamentadas.' },
  { icon: '🏢', title: 'Diagrama de FIIs', description: 'Análise de fundos imobiliários com perguntas focadas em vacância, dividend yield, P/VP e diversificação.' },
  { icon: '❓', title: 'Perguntas Personalizadas', description: 'Crie suas próprias perguntas binárias (Sim/Não) para personalizar completamente seu processo de análise.' },
  { icon: '🌍', title: 'Histórico Comunitário', description: 'Acesse os resultados de processamento de outros investidores e compartilhe suas análises com a comunidade.' },
  { icon: '🔒', title: 'Segurança em Primeiro Lugar', description: 'Suas chaves de API são encriptadas com criptografia Fernet. Login seguro via OAuth2 do Google.' }
]

const steps = [
  { title: 'Faça Login', description: 'Entre com sua conta Google em segundos. Cadastre um nickname e sua API Key do Gemini.' },
  { title: 'Selecione o Ativo', description: 'Escolha entre ações ou FIIs da B3. Selecione as perguntas padrão ou use as suas.' },
  { title: 'Receba sua Análise', description: 'Em poucos segundos, o Gemini processa e retorna as respostas fundamentadas para cada pergunta.' }
]

const handleGoogleLogin = async () => {
  // For now, we trigger the Google Sign-In flow.
  // This requires the Google Identity Services library.
  if (!import.meta.client || googleLoginLoading.value) return

  googleLoginLoading.value = true
  try {
    const google = (window as unknown as { google: unknown }).google as { accounts: { id: { initialize: (config: unknown) => void; prompt: () => void } } }
    if (!google) {
      // Fallback: load the script
      modalStore.showAlert('O serviço do Google está carregando. Tente novamente em instantes.', 'info')
      return
    }
    google.accounts.id.initialize({
      client_id: useRuntimeConfig().public.googleClientId,
      callback: handleCredentialResponse
    })
    google.accounts.id.prompt()
  } catch (e) {
    console.error('Google login error:', e)
  } finally {
    googleLoginLoading.value = false
  }
}

const handleCredentialResponse = async (response: { credential: string }) => {
  try {
    const data = await authStore.loginWithGoogle(response.credential)

    // Check if user needs onboarding
    if (!data.user_info.nickname) {
      showNicknameModal.value = true
    } else if (!data.user_info.has_gemini_key) {
      showApiKeyModal.value = true
    } else {
      navigateTo('/dashboard')
    }
  } catch (error: unknown) {
    console.error('Login failed:', error)
    modalStore.showAlert('Falha no login: ' + ((error as Error).message || 'Erro desconhecido'), 'error')
  }
}

const submitNickname = async () => {
  if (!nickname.value.trim()) return
  nicknameError.value = ''
  nicknameLoading.value = true

  try {
    await authStore.saveNickname(nickname.value.trim())
    showNicknameModal.value = false

    // Next step: API Key
    if (!authStore.user?.has_gemini_key) {
      showApiKeyModal.value = true
    } else {
      navigateTo('/dashboard')
    }
  } catch (error: unknown) {
    nicknameError.value = (error as Error).message || 'Falha ao validar nickname. Tente outro.'
  } finally {
    nicknameLoading.value = false
  }
}

const submitApiKey = async () => {
  if (!apiKey.value.trim()) return
  apiKeyError.value = ''
  apiKeyLoading.value = true

  try {
    await authStore.saveApiKey(apiKey.value.trim())
    showApiKeyModal.value = false
    navigateTo('/dashboard')
  } catch (error: unknown) {
    apiKeyError.value = (error as Error).message || 'Falha ao salvar chave.'
  } finally {
    apiKeyLoading.value = false
  }
}

const skipApiKey = () => {
  showApiKeyModal.value = false
  navigateTo('/dashboard')
}

// Load Google Identity Services script
if (import.meta.client) {
  useHead({
    script: [
      {
        src: 'https://accounts.google.com/gsi/client',
        async: true,
        defer: true
      }
    ]
  })
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .bg-brand-surface,
.modal-leave-to .bg-brand-surface {
  transform: scale(0.95) translateY(10px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}
.slide-enter-to,
.slide-leave-from {
  max-height: 500px;
}
</style>
