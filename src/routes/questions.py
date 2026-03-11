from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.core.security import get_current_user
from src.db.mongodb import get_database
from src.models.schemas import PyObjectId, Question, User

router = APIRouter()


class QuestionCreate(BaseModel):
    text: str = Field(..., max_length=500, description="The content of the question")
    type: str = Field(..., description="Type: 'stocks' or 'real_estate_funds'")


class QuestionUpdate(BaseModel):
    text: str = Field(..., max_length=500, description="The content of the question")


class QuestionResponse(BaseModel):
    id: str
    text: str
    type: str
    created_at: str


@router.get("/", response_model=list[QuestionResponse])
async def get_user_questions(
    type: str | None = None, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    query = {"user_id": current_user["_id"]}
    if type:
        if type not in ["stocks", "real_estate_funds"]:
            raise HTTPException(status_code=400, detail="Invalid type filter")
        query["type"] = type

    cursor = db["questions"].find(query)
    questions = await cursor.to_list(length=100)

    return [
        QuestionResponse(id=str(q["_id"]), text=q["text"], type=q["type"], created_at=q["created_at"].isoformat())
        for q in questions
    ]


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    if question.type not in ["stocks", "real_estate_funds"]:
        raise HTTPException(status_code=400, detail="Type must be either 'stocks' or 'real_estate_funds'")

    new_question = Question(user_id=PyObjectId(current_user["_id"]), text=question.text, type=question.type)

    result = await db["questions"].insert_one(new_question.model_dump(by_alias=True, exclude={"id"}))

    return QuestionResponse(
        id=str(result.inserted_id),
        text=new_question.text,
        type=new_question.type,
        created_at=new_question.created_at.isoformat(),
    )


@router.patch("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: str, question: QuestionUpdate, current_user: User = Depends(get_current_user), db=Depends(get_database)
):
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid question ID format")

    query = {"_id": ObjectId(question_id), "user_id": current_user["_id"]}
    existing_question = await db["questions"].find_one(query)

    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")

    await db["questions"].update_one(query, {"$set": {"text": question.text}})

    return QuestionResponse(
        id=question_id,
        text=question.text,
        type=existing_question["type"],
        created_at=existing_question["created_at"].isoformat(),
    )


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid question ID format")

    result = await db["questions"].delete_one({"_id": ObjectId(question_id), "user_id": current_user["_id"]})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    return None
