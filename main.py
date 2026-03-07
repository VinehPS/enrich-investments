import sys
import json
from src.analyzer import InvestmentAnalyzer
from src.data import get_questions_by_diagram, get_unique_diagram_types

def main():
    print("================================================================")
    print("--- Analisador de Investimentos com Gemini (Search Grounding) ---")
    print("================================================================\n")
    
    try:
        analyzer = InvestmentAnalyzer()
    except Exception as e:
        print(f"Erro de configuração: {str(e)}")
        print("\nPasso a passo para resolver:")
        print("1. Crie um arquivo .env na raiz do projeto (copie o .env.example)")
        print("2. Obtenha uma API Key no Google AI Studio (aistudio.google.com)")
        print("3. Preencha a variável GEMINI_API_KEY no arquivo .env")
        sys.exit(1)
        
    ticker = input("Digite o ticker do ativo a ser avaliado (ex: WEGE3, MXRF11): ").strip().upper()
    if not ticker:
        print("Ticker inválido.")
        sys.exit(1)
        
    print("\nGrupos de análise disponíveis:")
    diagram_types = get_unique_diagram_types()
    for i, dtype in enumerate(diagram_types, 1):
        print(f"[{i}] {dtype}")
        
    choice = input("\nEscolha o número do tipo de análise para o ativo: ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(diagram_types):
            raise ValueError()
        selected_diagram = diagram_types[idx]
        
        if selected_diagram == 'diagrama-do-cerrado':
            asset_type = 'Ação'
        elif selected_diagram == 'investimentos-imobiliarios':
            asset_type = 'Fundo Imobiliário (FII)'
        else:
            asset_type = 'Ativo Financeiro'
            
    except (ValueError, IndexError):
        print("Escolha inválida. O programa será encerrado.")
        sys.exit(1)
        
    questions = get_questions_by_diagram(selected_diagram)
    
    print(f"\n[!] Iniciando pesquisa do ativo {ticker} ({asset_type})...")
    print(f"[!] Avaliando {len(questions)} critérios na web.")
    print("[!] Aguarde, isso pode levar de 15 a 45 segundos dependendo do modelo e das pesquisas...")
    
    try:
        resultado = analyzer.analyze_asset(ticker, questions, asset_type)
        
        print("\n\n" + "="*80)
        print(f" RESULTADO DA ANÁLISE DO ATIVO: {resultado.asset_ticker} ")
        print("="*80)
        
        for idx, res in enumerate(resultado.results, 1):
            print(f"\n[{idx}] Pergunta: {res.question}")
            answer_tag = f"✅ SIM" if res.answer.upper() == "SIM" else f"❌ NÃO"
            print(f"    Resposta: {answer_tag}")
            print(f"    Fundamentação: {res.justification}")
            
        print("\n" + "-" * 80)
        print(" RESUMO GERAL ")
        print("-" * 80)
        print(f"{resultado.summary}\n")
        
        # Salvando backup em JSON
        filename = f"resultado_{ticker.replace('/', '_')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(resultado.model_dump_json(indent=4))
            
        print("="*80)
        print(f"✓ Backup detalhado (JSON) foi salvo em: {filename}")
        print("="*80)
            
    except Exception as e:
        print(f"\n[X] Ocorreu um erro durante a processamento: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
