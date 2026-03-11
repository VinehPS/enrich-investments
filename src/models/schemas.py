from datetime import datetime
from typing import Any, Literal

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    google_id: str
    email: EmailStr
    name: str
    picture: str | None = None
    encrypted_gemini_key: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class Question(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    text: str = Field(..., max_length=500)
    type: str  # 'stocks' or 'real_estate_funds'
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class ProcessingResult(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ticker: str
    type: str
    user_id: PyObjectId
    questions_answers: list[dict[str, Any]]  # [{"question": "...", "answer": "...", "justification": "..."}]
    processing_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class TickerCache(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    stock_tickers: list[dict[str, str]]
    fund_tickers: list[dict[str, str]]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class InvestmentCriteria(BaseModel):
    id: str = Field(description="ID do critério")
    criterias: str = Field(description="Nome ou categoria do critério / indicador (ex: ROE, CAGR, DIVIDENDOS)")
    question: str = Field(description="A pergunta que deve ser respondida com Sim ou Não")
    diagram: str = Field(
        description="O tipo de diagrama à qual a pergunta se destina (diagrama-do-cerrado para ações ou investimentos-imobiliarios para FIIs)"
    )


class CriteriaAnalysis(BaseModel):
    id: str = Field(description="ID do critério avaliado")
    question: str = Field(description="A pergunta respondida")
    answer: Literal["Sim", "Não"] = Field(
        description="A resposta estrita e objetiva baseada nos dados encontrados na web (DEVE ser 'Sim' ou 'Não')."
    )
    justification: str = Field(
        description="Breve justificativa apresentando os dados e números reais encontrados na pesquisa que embasaram a resposta."
    )


class AssetAnalysisResult(BaseModel):
    asset_ticker: str = Field(description="O código/ticker do ativo analisado (ex: WEGE3, MXRF11)")
    results: list[CriteriaAnalysis] = Field(description="Lista com as avaliações para cada pergunta fornecida")
    summary: str = Field(
        description="Um resumo geral sobre a qualidade do ativo baseado nos dados obtidos e critérios avaliados."
    )
