<template>
  <div>
    <NuxtLoadingIndicator color="#eab308" :height="3" :throttle="200" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <AppModal />
    <div
      v-if="pageLoading"
      class="fixed inset-0 z-40 flex items-center justify-center bg-black/40 backdrop-blur-sm pointer-events-none"
    >
      <div class="flex flex-col items-center gap-3 text-gray-200">
        <svg class="animate-spin w-8 h-8 text-brand" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 0 1 8-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 0 1 4 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        <span class="text-sm">Carregando página...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppModal from '~/components/AppModal.vue'

const pageLoading = ref(false)

if (import.meta.client) {
  const router = useRouter()
  const indicator = useLoadingIndicator()

  router.beforeEach((to, from, next) => {
    indicator.start()
    pageLoading.value = true
    next()
  })

  router.afterEach(() => {
    indicator.finish()
    pageLoading.value = false
  })
}
</script>
