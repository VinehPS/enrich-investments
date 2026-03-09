import os

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field

from src.utils.crypto import decrypt_data


class AnswerResult(BaseModel):
    question: str = Field(description="The exact question that was asked")
    answer: str = Field(description="The definitive answer, strict 'Sim' or 'Não'")
    justification: str = Field(description="Detailed explanation with facts and numbers found via Google Search")


class AssetAnalysisResult(BaseModel):
    ticker: str = Field(description="The asset's ticker symbol")
    asset_type: str = Field(description="The asset type (stocks or real_estate_funds)")
    answers: list[AnswerResult] = Field(description="The list of answers and justifications")


class GeminiService:
    def __init__(self, encrypted_api_key: str):
        self.api_key = decrypt_data(encrypted_api_key)
        if not self.api_key:
            raise ValueError("Invalid or corrupted API Key")

        # Optional fallback to env var for testing, but prefers user's key
        if self.api_key == "test" and os.getenv("GEMINI_API_KEY"):
            self.api_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    async def analyze(self, ticker: str, asset_type: str, questions: list[dict]) -> dict:
        questions_formatted = ""
        for i, q in enumerate(questions, 1):
            quest = q.get("text", "")
            questions_formatted += f"ID: {i} | Pergunta: {quest}\n"

        system_instruction = f"""Você é um analista financeiro sênior especializado no mercado brasileiro de ações e fundos imobiliários.
Sua missão é avaliar rigorosamente o ativo '{ticker}' (que é um(a) {asset_type}) respondendo a uma lista estrita de perguntas.
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
            # 1. Generate content with Google Search Grounding
            search_response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}],  # Ativa o Google Search Grounding
                    temperature=0.2,
                ),
            )

            # 2. Structure the text output using Pydantic JSON schema
            struct_prompt = f"Converta a seguinte análise do ativo {ticker} exatamente para o formato JSON requisitado pelas instruções. Retenha os fatos, números e decisões (Sim/Não) intactos:\n\n{search_response.text}"

            struct_response = self.client.models.generate_content(
                model=self.model_name,
                contents=struct_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AssetAnalysisResult,
                    temperature=0.0,
                ),
            )

            if hasattr(struct_response, "parsed") and struct_response.parsed:
                return struct_response.parsed.model_dump()

            import json

            return json.loads(struct_response.text)

        except APIError as e:
            msg = str(e).lower()
            if "api key not valid" in msg or "invalid api key" in msg:
                raise ValueError("A chave da API do Gemini fornecida é inválida.")
            if "quota" in msg or "rate limit" in msg or "429" in msg:
                raise ValueError("A chave da API atingiu o limite de requisições ou cota. Tente novamente mais tarde.")
            raise ValueError(f"Erro na API do Gemini: {str(e)}")
        except ValueError as e:
            # Re-raise the custom ValueErrors
            raise e
        except Exception as e:
            raise Exception(f"Falha inesperada ao comunicar com o modelo: {str(e)}")
