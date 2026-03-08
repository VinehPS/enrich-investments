<template>
  <div class="min-h-screen bg-brand-bg">
    <!-- Top Navigation -->
    <nav class="sticky top-0 z-50 bg-brand-bg/80 backdrop-blur-xl border-b border-brand-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <NuxtLink to="/dashboard" class="flex items-center gap-3 group">
            <div class="w-9 h-9 bg-gradient-to-br from-brand to-brand-light rounded-lg flex items-center justify-center shadow-lg shadow-brand/20 group-hover:shadow-brand/40 transition-shadow">
              <span class="text-brand-bg font-bold text-lg">E</span>
            </div>
            <span class="text-xl font-bold text-white hidden sm:block">
              Enrich<span class="text-brand-light">Investments</span>
            </span>
          </NuxtLink>

          <!-- Navigation Links -->
          <div class="hidden md:flex items-center gap-1">
            <NuxtLink
              to="/dashboard"
              class="nav-link"
              active-class="nav-link-active"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
              Dashboard
            </NuxtLink>
            <NuxtLink
              to="/questions"
              class="nav-link"
              active-class="nav-link-active"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Minhas Perguntas
            </NuxtLink>
            <NuxtLink
              to="/history"
              class="nav-link"
              active-class="nav-link-active"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Meu Histórico
            </NuxtLink>
            <NuxtLink
              to="/global-history"
              class="nav-link"
              active-class="nav-link-active"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Histórico Global
            </NuxtLink>
          </div>

          <!-- User Profile Dropdown -->
          <div class="relative" v-if="authStore.user">
            <button
              @click="showProfileMenu = !showProfileMenu"
              class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-surface border border-brand-border hover:border-brand/50 transition-colors"
            >
              <img
                v-if="authStore.user.picture"
                :src="authStore.user.picture"
                :alt="authStore.user.name"
                class="w-7 h-7 rounded-full object-cover"
                referrerpolicy="no-referrer"
              />
              <div v-else class="w-7 h-7 rounded-full bg-brand/20 flex items-center justify-center">
                <span class="text-brand text-sm font-semibold">{{ authStore.user.name?.charAt(0) }}</span>
              </div>
              <span class="text-sm text-gray-300 hidden sm:block max-w-[120px] truncate">{{ authStore.user.nickname || authStore.user.name }}</span>
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>

            <!-- Dropdown -->
            <Transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-if="showProfileMenu"
                class="absolute right-0 mt-2 w-56 rounded-xl bg-brand-surface border border-brand-border shadow-2xl py-1 z-50"
              >
                <NuxtLink
                  to="/profile"
                  @click="showProfileMenu = false"
                  class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-white/5 hover:text-white transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                  Meu Perfil
                </NuxtLink>
                <hr class="border-brand-border my-1" />
                <button
                  @click="handleLogout"
                  class="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                  Sair
                </button>
              </div>
            </Transition>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="showMobileMenu = !showMobileMenu" class="md:hidden text-gray-400 hover:text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 -translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-1"
      >
        <div v-if="showMobileMenu" class="md:hidden border-t border-brand-border bg-brand-surface/50 backdrop-blur-xl">
          <div class="px-4 py-3 space-y-1">
            <NuxtLink to="/dashboard" class="mobile-nav-link" @click="showMobileMenu = false">Dashboard</NuxtLink>
            <NuxtLink to="/questions" class="mobile-nav-link" @click="showMobileMenu = false">Minhas Perguntas</NuxtLink>
            <NuxtLink to="/history" class="mobile-nav-link" @click="showMobileMenu = false">Meu Histórico</NuxtLink>
            <NuxtLink to="/global-history" class="mobile-nav-link" @click="showMobileMenu = false">Histórico Global</NuxtLink>
            <NuxtLink to="/profile" class="mobile-nav-link" @click="showMobileMenu = false">Meu Perfil</NuxtLink>
          </div>
        </div>
      </Transition>
    </nav>

    <!-- API Key Alert Banner -->
    <div v-if="authStore.user && !authStore.user.has_gemini_key" class="bg-amber-500/10 border-b border-amber-500/30">
      <div class="max-w-7xl mx-auto px-4 py-3 flex items-center gap-3">
        <svg class="w-5 h-5 text-amber-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
        <p class="text-sm text-amber-200">
          <strong>API Key não cadastrada.</strong> Cadastre sua chave de API para iniciar os processamentos.
          <NuxtLink to="/profile" class="underline font-semibold hover:text-amber-100 ml-1">Ir para Meu Perfil →</NuxtLink>
        </p>
      </div>
    </div>

    <!-- Page Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const showProfileMenu = ref(false)
const showMobileMenu = ref(false)

// Close dropdown on outside click
if (import.meta.client) {
  onMounted(() => {
    document.addEventListener('click', (e: MouseEvent) => {
      const target = e.target as HTMLElement
      if (!target.closest('.relative')) {
        showProfileMenu.value = false
      }
    })
  })
}

const handleLogout = async () => {
  showProfileMenu.value = false
  await authStore.logout()
  navigateTo('/')
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-2 px-3 py-2 text-sm text-gray-400 rounded-lg hover:bg-white/5 hover:text-white transition-all duration-200;
}
.nav-link-active {
  @apply bg-brand/10 text-brand-light;
}
.mobile-nav-link {
  @apply block px-3 py-2.5 text-sm text-gray-300 rounded-lg hover:bg-white/5 hover:text-white transition-colors;
}
</style>
