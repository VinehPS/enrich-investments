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


@router.post("/nickname")
async def set_nickname(
    request: NicknameRequest, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    nickname = request.nickname.strip()

    # Validate length
    if len(nickname) < 1 or len(nickname) > 25:
        raise HTTPException(status_code=400, detail="O nickname deve ter entre 1 e 25 caracteres.")

    # Validate characters (alphanumeric, underscores, hyphens)
    if not re.match(r"^[a-zA-Z0-9_\-]+$", nickname):
        raise HTTPException(
            status_code=400, detail="O nickname deve conter apenas letras, números, underscores e hífens."
        )

    # Check offensive content
    if is_offensive(nickname):
        raise HTTPException(
            status_code=400,
            detail="Este nickname contém termos ofensivos, agressivos ou discriminatórios e não é permitido.",
        )

    # Check uniqueness (case-insensitive)
    existing = await db["users"].find_one({"nickname": {"$regex": f"^{re.escape(nickname)}$", "$options": "i"}})
    if existing and str(existing["_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=409, detail="Este nickname já está em uso. Escolha outro.")

    # Save nickname
    await db["users"].update_one({"_id": current_user["_id"]}, {"$set": {"nickname": nickname}})

    return {"nickname": nickname, "message": "Nickname salvo com sucesso!"}


@router.get("/nickname")
async def get_nickname(current_user: User = Depends(get_current_user)):
    return {"nickname": current_user.get("nickname")}
