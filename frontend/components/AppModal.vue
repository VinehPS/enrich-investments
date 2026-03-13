<template>
  <Transition name="modal">
    <div
      v-if="modal.visible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      @keydown.esc.prevent="handleEsc"
    >
      <div
        ref="cardRef"
        class="w-full max-w-md bg-brand-surface border rounded-2xl p-6 shadow-2xl"
        :class="borderClass"
        tabindex="-1"
      >
        <div class="flex items-start gap-3">
          <div :class="iconWrapperClass">
            <span class="text-lg">
              <span v-if="modal.type === 'info'">ℹ️</span>
              <span v-else-if="modal.type === 'error'">⚠️</span>
              <span v-else>⚠️</span>
            </span>
          </div>
          <div class="flex-1">
            <h2 class="text-base font-semibold text-white mb-1">
              {{ title }}
            </h2>
            <p class="text-sm text-gray-300 whitespace-pre-line">
              {{ modal.message }}
            </p>

            <div class="mt-5 flex justify-end gap-3">
              <button
                v-if="modal.mode === 'confirm'"
                type="button"
                class="px-4 py-2 rounded-xl border border-brand-border text-sm text-gray-300 hover:bg-white/5 transition-colors"
                @click="onCancel"
              >
                Cancelar
              </button>
              <button
                ref="primaryButtonRef"
                type="button"
                class="px-4 py-2 rounded-xl text-sm font-semibold bg-gradient-to-r from-brand to-brand-dark text-brand-bg hover:brightness-110 transition-all shadow-lg shadow-brand/30"
                @click="onPrimary"
              >
                {{ primaryLabel }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, computed } from 'vue'
import { useModalStore } from '~/stores/modal'

const modal = useModalStore()

const cardRef = ref<HTMLElement | null>(null)
const primaryButtonRef = ref<HTMLButtonElement | null>(null)

const title = computed(() => {
  if (modal.mode === 'confirm') {
    if (modal.type === 'error') return 'Confirmar ação'
    if (modal.type === 'warning') return 'Tem certeza?'
    return 'Confirmação'
  }

  if (modal.type === 'error') return 'Algo deu errado'
  if (modal.type === 'warning') return 'Atenção'
  return 'Informação'
})

const primaryLabel = computed(() => (modal.mode === 'confirm' ? 'Confirmar' : 'OK'))

const borderClass = computed(() => {
  if (modal.type === 'error') return 'border-red-500/30'
  if (modal.type === 'warning') return 'border-amber-500/30'
  return 'border-brand-border'
})

const iconWrapperClass = computed(() => {
  if (modal.type === 'error') return 'w-9 h-9 rounded-xl bg-red-500/10 text-red-400 flex items-center justify-center'
  if (modal.type === 'warning') return 'w-9 h-9 rounded-xl bg-amber-500/10 text-amber-300 flex items-center justify-center'
  return 'w-9 h-9 rounded-xl bg-blue-500/10 text-blue-300 flex items-center justify-center'
})

const handleEsc = () => {
  if (!modal.visible) return
  if (modal.mode === 'confirm') {
    modal.resolveConfirm(false)
  } else {
    modal.resolveAlert()
  }
}

const onPrimary = () => {
  if (modal.mode === 'confirm') {
    modal.resolveConfirm(true)
  } else {
    modal.resolveAlert()
  }
}

const onCancel = () => {
  modal.resolveConfirm(false)
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    event.preventDefault()
    handleEsc()
  }
}

watch(
  () => modal.visible,
  visible => {
    if (visible) {
      setTimeout(() => {
        if (primaryButtonRef.value) {
          primaryButtonRef.value.focus()
        } else if (cardRef.value) {
          cardRef.value.focus()
        }
      }, 0)
    }
  }
)

onMounted(() => {
  if (import.meta.client) {
    window.addEventListener('keydown', handleKeydown)
  }
})

onUnmounted(() => {
  if (import.meta.client) {
    window.removeEventListener('keydown', handleKeydown)
  }
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .bg-brand-surface,
.modal-leave-to .bg-brand-surface {
  transform: scale(0.95) translateY(8px);
}
</style>

