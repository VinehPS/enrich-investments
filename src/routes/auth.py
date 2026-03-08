from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from bson import ObjectId
from src.core.config import settings
from src.core.security import verify_google_token, create_access_token, get_current_user
from src.db.mongodb import get_database
from src.models.schemas import User
from src.utils.crypto import encrypt_data

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

class GeminiKeyRequest(BaseModel):
    gemini_key: str

@router.post("/login", response_model=TokenResponse)
async def login_google_oauth2(request: GoogleAuthRequest, db=Depends(get_database)):
    # 1. Verify Google Token
    idinfo = await verify_google_token(request.token)
    if not idinfo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google Token",
        )
    
    google_id = idinfo['sub']
    email = idinfo['email']
    name = idinfo.get('name', '')
    picture = idinfo.get('picture', None)

    # 2. Find or Create User
    users_collection = db["users"]
    user = await users_collection.find_one({"google_id": google_id})
    
    if not user:
        new_user = User(google_id=google_id, email=email, name=name, picture=picture)
        result = await users_collection.insert_one(new_user.model_dump(by_alias=True, exclude={"id"}))
        user_id = str(result.inserted_id)
        user_data = new_user.model_dump()
    else:
        user_id = str(user["_id"])
        user_data = user

    # 3. Create Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id, "email": email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_info": {
            "email": email, 
            "name": name, 
            "picture": picture,
            "has_gemini_key": bool(user_data.get("encrypted_gemini_key"))
        }
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    # Stateless JWT -> Frontend discards token. 
    # To implement strict server-side logout, we'd need a token blacklist in DB/Redis.
    return {"message": "Successfully logged out. Please remove token from local storage."}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "name": current_user["name"],
        "has_gemini_key": bool(current_user.get("encrypted_gemini_key"))
    }

@router.delete("/me")
async def delete_user_account(current_user: User = Depends(get_current_user), db=Depends(get_database)):
    user_id = current_user["_id"]
    # 1. Delete user
    await db["users"].delete_one({"_id": user_id})
    # 2. Delete related user data
    await db["questions"].delete_many({"user_id": user_id})
    await db["processings"].delete_many({"user_id": user_id})
    return {"message": "Account and all associated historical data deleted successfully"}

@router.post("/gemini-key")
async def save_gemini_key(request: GeminiKeyRequest, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    if not request.gemini_key:
        raise HTTPException(status_code=400, detail="Gemini key cannot be empty")
        
    encrypted_key = encrypt_data(request.gemini_key)
    if not encrypted_key:
        raise HTTPException(status_code=500, detail="Failed to encrypt key due to server configuration")
        
    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": {"encrypted_gemini_key": encrypted_key}}
    )
    
    return {"message": "Gemini Key securely encrypted and saved"}
