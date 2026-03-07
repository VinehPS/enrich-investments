from pydantic import BaseModel, Field
from typing import Literal

class InvestmentCriteria(BaseModel):
    id: str = Field(description="ID do critério")
    criterias: str = Field(description="Nome ou categoria do critério / indicador (ex: ROE, CAGR, DIVIDENDOS)")
    question: str = Field(description="A pergunta que deve ser respondida com Sim ou Não")
    diagram: str = Field(description="O tipo de diagrama à qual a pergunta se destina (diagrama-do-cerrado para ações ou investimentos-imobiliarios para FIIs)")

class CriteriaAnalysis(BaseModel):
    id: str = Field(description="ID do critério avaliado")
    question: str = Field(description="A pergunta respondida")
    answer: Literal["Sim", "Não"] = Field(description="A resposta estrita e objetiva baseada nos dados encontrados na web (DEVE ser 'Sim' ou 'Não').")
    justification: str = Field(description="Breve justificativa apresentando os dados e números reais encontrados na pesquisa que embasaram a resposta.")

class AssetAnalysisResult(BaseModel):
    asset_ticker: str = Field(description="O código/ticker do ativo analisado (ex: WEGE3, MXRF11)")
    results: list[CriteriaAnalysis] = Field(description="Lista com as avaliações para cada pergunta fornecida")
    summary: str = Field(description="Um resumo geral sobre a qualidade do ativo baseado nos dados obtidos e critérios avaliados.")
