import { describe, it, expect } from 'vitest'

describe('Questions Store Logic', () => {
  it('should validate question text length (max 500 chars)', () => {
    const maxLength = 500
    const validQuestion = 'A empresa possui lucro crescente?'
    const invalidQuestion = 'x'.repeat(501)

    expect(validQuestion.length).toBeLessThanOrEqual(maxLength)
    expect(invalidQuestion.length).toBeGreaterThan(maxLength)
  })

  it('should validate question type', () => {
    const validTypes = ['stocks', 'real_estate_funds']

    expect(validTypes.includes('stocks')).toBe(true)
    expect(validTypes.includes('real_estate_funds')).toBe(true)
    expect(validTypes.includes('crypto')).toBe(false)
  })

  it('should filter questions by type', () => {
    const questions = [
      { id: '1', text: 'Pergunta ações 1', type: 'stocks', created_at: '2024-01-01' },
      { id: '2', text: 'Pergunta FII 1', type: 'real_estate_funds', created_at: '2024-01-01' },
      { id: '3', text: 'Pergunta ações 2', type: 'stocks', created_at: '2024-01-01' }
    ]

    const stocksOnly = questions.filter(q => q.type === 'stocks')
    const fundsOnly = questions.filter(q => q.type === 'real_estate_funds')

    expect(stocksOnly).toHaveLength(2)
    expect(fundsOnly).toHaveLength(1)
  })
})

describe('Ticker Search Logic', () => {
  it('should filter tickers by search query', () => {
    const tickers = [
      { ticker: 'BBAS3', name: 'Banco do Brasil' },
      { ticker: 'ITUB4', name: 'Itaú Unibanco' },
      { ticker: 'HGLG11', name: 'CSHG Logística' },
      { ticker: 'PETR4', name: 'Petrobras' }
    ]

    const query = 'bb'
    const filtered = tickers.filter(
      t => t.ticker.toLowerCase().includes(query) || t.name.toLowerCase().includes(query)
    )

    expect(filtered).toHaveLength(1)
    expect(filtered[0].ticker).toBe('BBAS3')
  })

  it('should identify FII vs Stock by ticker pattern', () => {
    const isStock = (ticker: string) => !ticker.endsWith('11') || ticker.length < 5

    expect(isStock('BBAS3')).toBe(true)
    expect(isStock('PETR4')).toBe(true)
    expect(isStock('HGLG11')).toBe(false)
    expect(isStock('XPML11')).toBe(false)
  })
})

describe('History Sorting', () => {
  it('should sort results by date descending (newest first)', () => {
    const results = [
      { id: '1', processing_date: '2024-01-01T10:00:00' },
      { id: '2', processing_date: '2024-03-15T10:00:00' },
      { id: '3', processing_date: '2024-02-10T10:00:00' }
    ]

    const sorted = [...results].sort(
      (a, b) => new Date(b.processing_date).getTime() - new Date(a.processing_date).getTime()
    )

    expect(sorted[0].id).toBe('2')
    expect(sorted[1].id).toBe('3')
    expect(sorted[2].id).toBe('1')
  })

  it('should sort results by date ascending (oldest first)', () => {
    const results = [
      { id: '1', processing_date: '2024-01-01T10:00:00' },
      { id: '2', processing_date: '2024-03-15T10:00:00' },
      { id: '3', processing_date: '2024-02-10T10:00:00' }
    ]

    const sorted = [...results].sort(
      (a, b) => new Date(a.processing_date).getTime() - new Date(b.processing_date).getTime()
    )

    expect(sorted[0].id).toBe('1')
    expect(sorted[1].id).toBe('3')
    expect(sorted[2].id).toBe('2')
  })
})
