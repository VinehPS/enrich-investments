import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.models import AssetAnalysisResult

load_dotenv()


class InvestmentAnalyzer:
    def __init__(self):
        """
        Inicializa o analisador validando a chave de API e instanciando o client do Gemini.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "COLOQUE_SUA_API_KEY_AQUI":
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env ou usando a chave padrão.")

        self.client = genai.Client(api_key=api_key)
        # Utilizando o gemini-2.5-flash: rápido, econômico e suporta Search Grounding nativo + Structured Outputs
        self.model_name = "gemini-2.5-flash"

    def analyze_asset(self, ticker: str, questions: list[dict], asset_type: str) -> AssetAnalysisResult:
        """
        Analisa um ativo com base nas perguntas fornecidas usando Gemini e Google Search.
        Retorna o resultado no formato estruturado do Pydantic (AssetAnalysisResult).
        """

        # Prepara a lista de perguntas para o prompt
        questions_formatted = ""
        for i, q in enumerate(questions, 1):
            crit = q.get("criterias", "Critério Geral")
            quest = q.get("question", "")
            q_id = q.get("_id", str(i))
            questions_formatted += f"ID: {q_id} | Critério: {crit} | Pergunta: {quest}\n"

        system_instruction = f"""Você é um analista financeiro sênior especializado no mercado brasileiro de ações e fundos imobiliários.
Sua missão é avaliar rigorosamente o ativo '{ticker}' (que é um(a) {asset_type}) respondendo a uma lista estrita de perguntas para um framework de investimento.
Para cada pergunta, você DEVE buscar os dados mais recentes na internet usando a ferramenta de pesquisa do Google antes de responder.
A resposta final (answer) para cada pergunta DEVE ser estritamente 'Sim' ou 'Não'.
Sempre inclua os dados numéricos exatos, indicadores e fatos recentes encontrados na pesquisa na sua 'justification'.
"""

        prompt = f"""Ativo a ser analisado: {ticker}

Por favor, analise e responda 'Sim' ou 'Não' para cada uma das perguntas abaixo buscando informações atualizadas na internet.

Lista de Perguntas (Critérios de Avaliação):
{questions_formatted}
"""

        try:
            # Passo 1: Geração de conteúdo com Google Search (Sem Structured Outputs JSON)
            search_response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}],  # Ativa o Google Search Grounding
                    temperature=0.2,  # Temperatura baixa para focar em fatos concretos
                ),
            )

            # Passo 2: Estruturar a resposta com JSON Schema (Sem Search)
            struct_prompt = f"Converta a seguinte análise do ativo {ticker} extamente para o formato JSON requisitado pelas instruções. Retenha os fatos, números e decisões (Sim/Não) intactos:\n\n{search_response.text}"

            struct_response = self.client.models.generate_content(
                model=self.model_name,
                contents=struct_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AssetAnalysisResult,
                    temperature=0.0,  # Temperatura mínima para formatação estrita
                ),
            )

            # Quando response_schema é fornecido, response.parsed conterá o objeto Python instanciado (Pydantic)
            return struct_response.parsed

        except Exception as e:
            raise Exception(f"Falha ao comunicar com a API do Gemini: {str(e)}")
