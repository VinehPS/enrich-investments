import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { defineConfig as defineVitestConfig, mergeConfig } from 'vitest/config'

const viteConfig = defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '~/': resolve(__dirname, './'),
      '#imports': resolve(__dirname, '.nuxt/imports.d.ts')
    }
  }
})

export default mergeConfig(
  viteConfig,
  defineVitestConfig({
    test: {
      globals: true,
      environment: 'jsdom'
    }
  })
)
