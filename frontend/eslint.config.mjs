// https://nuxt.com/docs/guide/concepts/eslint
import { createConfigForNuxt } from '@nuxt/eslint-config/flat'
import prettierConfig from 'eslint-config-prettier'
import prettierPlugin from 'eslint-plugin-prettier'

export default createConfigForNuxt({
  plugins: {
    prettier: prettierPlugin
  },
  rules: {
    'prettier/prettier': 'error'
  }
}).append(prettierConfig)
