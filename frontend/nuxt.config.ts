// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: true,
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt'
  ],
  css: [
    '~/assets/css/main.css'
  ],
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
      googleClientId: process.env.NUXT_PUBLIC_GOOGLE_CLIENT_ID || ''
    }
  },
  app: {
    baseURL: process.env.NUXT_APP_BASE_URL || '/',
    head: {
      htmlAttrs: { lang: 'pt-BR' },
      title: 'Enrich Investments',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Plataforma de enriquecimento de dados para o Diagrama do Cerrado e Diagrama de FIIs. Análise automatizada com Google Gemini AI.' },
        { name: 'keywords', content: 'investimentos, ações, FIIs, fundos imobiliários, diagrama do cerrado, análise fundamentalista, inteligência artificial, Gemini' },
        { property: 'og:title', content: 'Enrich Investments — Análise de Ações e FIIs com IA' },
        { property: 'og:description', content: 'Preencha automaticamente seu Diagrama do Cerrado e de FIIs com IA.' },
        { property: 'og:type', content: 'website' }
      ],
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
        }
      ]
    }
  },
  nitro: {
    preset: 'github-pages'
  }
})
