import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.core.security import get_current_user
from src.db.mongodb import get_database
from src.models.schemas import User

router = APIRouter()


class NicknameRequest(BaseModel):
    nickname: str = Field(..., max_length=25, min_length=1, description="User nickname, max 25 characters")


# Basic profanity/offensive words regex filter (Portuguese + English)
# In production, this would call Gemini for content moderation
OFFENSIVE_PATTERNS = [
    r"\b(porra|caralho|merda|foda|puta|viado|viada|bicha|corno|arrombado|desgraca|imbecil|idiota|retardado|mongoloide|negro[s]?\s*(lixo|nojento)|macaco|preto[s]?\s*(imundo|nojento))\b",
    r"\b(fuck|shit|ass|dick|bitch|nigger|faggot|retard|racist|nazi|hitler)\b",
]


def is_offensive(text: str) -> bool:
    """Check if text contains offensive content using regex patterns."""
    lowered = text.lower().strip()
    for pattern in OFFENSIVE_PATTERNS:
        if re.search(pattern, lowered, re.IGNORECASE):
            return True
    return False


from src.services.gemini import GeminiService


@router.post("/nickname")
async def set_nickname(
    request: NicknameRequest, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    nickname = request.nickname.strip()

    # 1. Basic format validation (length, characters)
    if len(nickname) < 1 or len(nickname) > 25:
        raise HTTPException(status_code=400, detail="O nickname deve ter entre 1 e 25 caracteres.")

    if not re.match(r"^[a-zA-Z0-9_\-]+$", nickname):
        raise HTTPException(
            status_code=400, detail="O nickname deve conter apenas letras, números, underscores e hífens."
        )

    # 2. AI Moderation (Gemini)
    try:
        # Use user's key if available, otherwise GeminiService falls back to system key in .env
        gemini = GeminiService(current_user.get("encrypted_gemini_key"))
        validation = await gemini.validate_nickname(nickname)
        
        if not validation.get("is_valid"):
            reason = validation.get("reason") or "Nickname inapropriado."
            raise HTTPException(status_code=400, detail=f"IA: {reason}")
    except ValueError as e:
        # Fallback to current regex if Gemini is not configured, but log it
        print(f"AVISO: Pulando validação por IA devido a erro de configuração: {str(e)}")
        if is_offensive(nickname):
            raise HTTPException(
                status_code=400,
                detail="Este nickname contém termos offensivos e não é permitido.",
            )
    except Exception as e:
        print(f"ERRO NA VALIDAÇÃO POR IA: {str(e)}")

    # 3. Check uniqueness (case-insensitive)
    existing = await db["users"].find_one({"nickname": {"$regex": f"^{re.escape(nickname)}$", "$options": "i"}})
    if existing and str(existing["_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=409, detail="Este nickname já está em uso. Escolha outro.")

    # Save nickname
    await db["users"].update_one({"_id": current_user["_id"]}, {"$set": {"nickname": nickname}})

    return {"nickname": nickname, "message": "Nickname salvo com sucesso!"}


@router.get("/nickname")
async def get_nickname(current_user: User = Depends(get_current_user)):
    return {"nickname": current_user.get("nickname")}
