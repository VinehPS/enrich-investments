from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

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
    picture: Optional[str] = None
    encrypted_gemini_key: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class Question(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    text: str = Field(..., max_length=500)
    type: str # 'stocks' or 'real_estate_funds'
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class ProcessingResult(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ticker: str
    type: str
    user_id: PyObjectId
    questions_answers: List[Dict[str, Any]] # [{"question": "...", "answer": "...", "justification": "..."}]
    processing_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class TickerCache(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    stock_tickers: List[Dict[str, str]]
    fund_tickers: List[Dict[str, str]]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
