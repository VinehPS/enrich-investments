from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from src.core.security import get_current_user
from src.db.mongodb import get_database
from src.models.schemas import ProcessingResult, PyObjectId, User
from src.services.gemini import GeminiService

router = APIRouter()


class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., description="Asset ticker, e.g., BBAS3")
    type: str = Field(..., description="'stocks' or 'real_estate_funds'")
    questions: list[dict] | None = Field(None, description="Optional custom questions. If null, uses defaults.")


class AnalyzeResponse(BaseModel):
    id: str
    ticker: str
    type: str
    questions_answers: list[dict]
    processing_date: str


DEFAULT_STOCKS_QUESTIONS = [
    {"text": "A empresa apresentou lucro líquido consistente e crescente nos últimos 5 anos?"},
    {"text": "A margem líquida da empresa é superior a 10% atualmente?"},
    {"text": "O ROE (Retorno sobre Patrimônio Líquido) da empresa está acima de 15%?"},
    {"text": "A relação Dívida Líquida / EBITDA é menor que 3.0x?"},
    {"text": "A empresa tem um histórico de pagamento de dividendos ininterrupto nos últimos 5 anos?"},
]

DEFAULT_FUNDS_QUESTIONS = [
    {"text": "O fundo possui um Dividend Yield atual acima da taxa Selic (ou comparável a ela) nos últimos 12 meses?"},
    {"text": "O fundo possui P/VP (Preço sobre Valor Patrimonial) próximo ou inferior a 1.05?"},
    {"text": "O fundo apresenta baixa vacância física e financeira histórica (abaixo de 10%)?"},
    {"text": "O fundo é diversificado, possuindo múltiplos imóveis/ativos e inquilinos?"},
    {"text": "O fundo não possui histórico de calotes sistêmicos recentes nos CRIs ou aluguéis?"},
]


@router.post("/", response_model=AnalyzeResponse)
async def analyze_asset(
    request: AnalyzeRequest, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    if request.type not in ["stocks", "real_estate_funds"]:
        raise HTTPException(status_code=400, detail="Type must be 'stocks' or 'real_estate_funds'")

    encrypted_key = current_user.get("encrypted_gemini_key")
    if not encrypted_key:
        raise HTTPException(
            status_code=400, detail="Gemini API Key not configured for this user. Please save it in your profile first."
        )

    questions_to_ask = request.questions

    # Use defaults if none provided
    if not questions_to_ask or len(questions_to_ask) == 0:
        if request.type == "stocks":
            questions_to_ask = DEFAULT_STOCKS_QUESTIONS
        else:
            questions_to_ask = DEFAULT_FUNDS_QUESTIONS

    try:
        service = GeminiService(encrypted_key)
        result_dict = await service.analyze(request.ticker, request.type, questions_to_ask)

        # Format the result correctly
        if "answers" in result_dict:
            answers_list = result_dict["answers"]
        else:
            answers_list = result_dict.get("questions_answers", [])

        processing_date = datetime.utcnow()

        # Save to database
        db_result = ProcessingResult(
            ticker=request.ticker.upper(),
            type=request.type,
            user_id=PyObjectId(current_user["_id"]),
            questions_answers=answers_list,
            processing_date=processing_date,
        )

        insert_res = await db["processings"].insert_one(db_result.model_dump(by_alias=True, exclude={"id"}))

        return AnalyzeResponse(
            id=str(insert_res.inserted_id),
            ticker=db_result.ticker,
            type=db_result.type,
            questions_answers=db_result.questions_answers,
            processing_date=db_result.processing_date.isoformat(),
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/history", response_model=list[AnalyzeResponse])
async def get_general_history(
    ticker: str | None = Query(None, description="Filtro opcional por ticker"),
    type: str | None = Query(None, description="Filtro opcional por tipo"),
    start_date: str | None = Query(None, description="Filtro inicial de data (ISO)"),
    current_user: User = Depends(get_current_user),
    db=Depends(get_database),
):
    query = {"user_id": current_user["_id"]}

    if ticker:
        query["ticker"] = ticker.upper()
    if type:
        query["type"] = type
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            query["processing_date"] = {"$gte": start_dt}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use ISO format.")

    cursor = db["processings"].find(query).sort("processing_date", -1)
    results = await cursor.to_list(length=100)

    return [
        AnalyzeResponse(
            id=str(r["_id"]),
            ticker=r["ticker"],
            type=r["type"],
            questions_answers=r["questions_answers"],
            processing_date=r["processing_date"].isoformat(),
        )
        for r in results
    ]


@router.get("/history/{type}/{ticker}", response_model=list[AnalyzeResponse])
async def get_specific_history(
    type: str, ticker: str, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    if type not in ["stocks", "real_estate_funds"]:
        raise HTTPException(status_code=400, detail="Type must be 'stocks' or 'real_estate_funds'")

    query = {"user_id": current_user["_id"], "ticker": ticker.upper(), "type": type}

    cursor = db["processings"].find(query).sort("processing_date", -1)
    results = await cursor.to_list(length=100)

    return [
        AnalyzeResponse(
            id=str(r["_id"]),
            ticker=r["ticker"],
            type=r["type"],
            questions_answers=r["questions_answers"],
            processing_date=r["processing_date"].isoformat(),
        )
        for r in results
    ]


@router.get("/default-questions")
async def get_default_questions():
    return {"stocks": DEFAULT_STOCKS_QUESTIONS, "real_estate_funds": DEFAULT_FUNDS_QUESTIONS}
