from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.core.security import get_current_user
from src.db.mongodb import get_database
from src.models.schemas import User

router = APIRouter()


class GlobalHistoryResponse(BaseModel):
    id: str
    ticker: str
    type: str
    questions_answers: list
    processing_date: str
    nickname: str | None = None


@router.get("/global", response_model=list[GlobalHistoryResponse])
async def get_global_history(
    search: str | None = Query(None, description="Search in ticker or question text"),
    type: str | None = Query(None, description="Filter by type: stocks or real_estate_funds"),
    sort: str | None = Query("newest", description="Sort order: newest or oldest"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    """
    Get global processing history from all users.
    NEVER returns google_id or api_key.
    Shows nickname of the processing author.
    """
    pipeline = []

    # Match filters
    match_stage: dict = {}
    if type and type in ["stocks", "real_estate_funds"]:
        match_stage["type"] = type
    if search:
        match_stage["$or"] = [
            {"ticker": {"$regex": search, "$options": "i"}},
            {"questions_answers.question": {"$regex": search, "$options": "i"}},
        ]

    if match_stage:
        pipeline.append({"$match": match_stage})

    # Sort
    sort_dir = 1 if sort == "oldest" else -1
    pipeline.append({"$sort": {"processing_date": sort_dir}})

    # Pagination
    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": limit})

    # Lookup user to get nickname (NEVER expose google_id or encrypted_gemini_key)
    pipeline.append({"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user_info"}})

    # Unwind user info
    pipeline.append({"$unwind": {"path": "$user_info", "preserveNullAndEmptyArrays": True}})

    # Project only safe fields
    pipeline.append(
        {
            "$project": {
                "_id": 1,
                "ticker": 1,
                "type": 1,
                "questions_answers": 1,
                "processing_date": 1,
                "nickname": "$user_info.nickname",
                # Explicitly NOT including: google_id, email, encrypted_gemini_key
            }
        }
    )

    cursor = db["processings"].aggregate(pipeline)
    results = await cursor.to_list(length=limit)

    return [
        GlobalHistoryResponse(
            id=str(r["_id"]),
            ticker=r["ticker"],
            type=r["type"],
            questions_answers=r["questions_answers"],
            processing_date=r["processing_date"].isoformat()
            if isinstance(r["processing_date"], datetime)
            else r["processing_date"],
            nickname=r.get("nickname"),
        )
        for r in results
    ]
