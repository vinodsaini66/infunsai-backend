from fastapi import APIRouter, Request, HTTPException
from app.db.mongo import db
from app.schemas.user_schema import UserAccountType, UserOut
from bson import ObjectId
from app.models.user_model import User
from datetime import datetime

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_me(request: Request):
    user_data = request.state.user
    user = await User.find_one({"_id": ObjectId(user_data["sub"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/", response_model=list[UserOut])
async def list_users(request: Request):
    user_data = request.state.user
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    cursor = db.users.find({})
    users = []
    async for u in cursor:
        u["_id"] = str(u["_id"])
        users.append(u)
    return users


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update Post
@router.post("/account_type")
async def update_account_type(data: UserAccountType, request: Request):
    user = request.state.user
    print("User from token:", data)
    user_data = await User.find_one({"_id": ObjectId(user["sub"])})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only account_type
    user_data.account_type = data.account_type
    user_data.updated_at = datetime.now()

    await user_data.save()

    return {
        "message": "Account type updated successfully",
        "status": True
    }