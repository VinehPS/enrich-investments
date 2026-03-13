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


class NicknameValidationResult(BaseModel):
    is_valid: bool = Field(description="True se o nickname for apropriado, False caso contrário")
    reason: str | None = Field(description="Motivo da rejeição em português, se houver")


class GeminiService:
    def __init__(self, encrypted_api_key: str | None = None):
        self.api_key: str | None = None
        if encrypted_api_key:
            self.api_key = decrypt_data(encrypted_api_key)
        
        # Fallback to env var if no key provided or decryption failed
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("Nenhuma API Key do Gemini configurada no sistema ou no usuário.")

        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash"

    async def validate_nickname(self, nickname: str) -> dict:
        """Valida se um nickname é apropriado usando IA."""
        system_instruction = """Você é um moderador de conteúdo especializado em comunidades de investimento.
Sua missão é avaliar se um nickname escolhido por um usuário é apropriado para uma plataforma pública e respeitosa.
REGRAS DE REJEIÇÃO:
1. Conteúdo racista, homofóbico, sexista ou discriminatório.
2. Palavrões pesados ou termos agressivos.
3. Incitação ao ódio ou violência.
4. Nomes que tentam burlar filtros (ex: usando hífens ou números para formar palavras proibidas).
5. Nomes de figuras históricas infames (ex: ditadores).
Nomes de memes financeiros, termos de bolsa (ex: 'BuyAndHold', 'FII_Lover') ou nicknames criativos normais são PERMITIDOS.
Você deve responder estritamente no formato JSON definido."""

        prompt = f"Avalie o seguinte nickname para uso na plataforma: '{nickname}'"

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=NicknameValidationResult,
                    temperature=0.0,
                ),
            )
            
            if hasattr(response, "parsed") and response.parsed:
                return response.parsed.model_dump()
            
            import json
            return json.loads(response.text)
        except Exception as e:
            # Fallback em caso de erro na API: permitir para não travar o usuário, 
            # assumindo que o regex básico no router ainda vai rodar.
            print(f"ERRO NA VALIDAÇÃO DE NICKNAME COM IA: {str(e)}")
            return {"is_valid": True, "reason": None}

    async def analyze(self, ticker: str, asset_type: str, questions: list[dict]) -> dict:
        # ... (rest of the file remains similar, but using self.model_name)
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
