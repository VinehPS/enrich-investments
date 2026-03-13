import { defineStore } from 'pinia'

type ModalMode = 'alert' | 'confirm'
type ModalType = 'info' | 'error' | 'warning'

interface ModalState {
  visible: boolean
  mode: ModalMode
  type: ModalType
  message: string
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  resolver: ((value: any) => void) | null
}

export const useModalStore = defineStore('modal', {
  state: (): ModalState => ({
    visible: false,
    mode: 'alert',
    type: 'info',
    message: '',
    resolver: null
  }),

  actions: {
    reset() {
      this.visible = false
      this.mode = 'alert'
      this.type = 'info'
      this.message = ''
      this.resolver = null
    },

    showAlert(message: string, type: ModalType = 'info'): Promise<void> {
      this.mode = 'alert'
      this.type = type
      this.message = message
      this.visible = true

      return new Promise(resolve => {
        this.resolver = resolve
      })
    },

    showConfirm(message: string, type: ModalType = 'warning'): Promise<boolean> {
      this.mode = 'confirm'
      this.type = type
      this.message = message
      this.visible = true

      return new Promise(resolve => {
        this.resolver = resolve
      })
    },

    resolveAlert() {
      if (this.resolver) {
        this.resolver(undefined)
      }
      this.reset()
    },

    resolveConfirm(result: boolean) {
      if (this.resolver) {
        this.resolver(result)
      }
      this.reset()
    }
  }
})

