from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.mongo import db
from app.schemas.user_schema import UserCreate, UserOut,UserLogin
from app.schemas.token_schema import Token
from app.utils.password import hash_password, verify_password 
from app.core.security import create_access_token
from bson import ObjectId
from datetime import timedelta
from app.models.user_model import User
from app.models.linkedin_model import LinkedinConnect
from app.core.config import settings

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    full_name= user.first_name + " " + user.last_name
    new_user = User(email=user.email,
                    password=hashed_pw, 
                    first_name=user.first_name,
                    last_name=user.last_name,
                    full_name=full_name,
                    company_name=user.company_name,
                    role=user.role
                    )
    await new_user.insert() 
    
    access_token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/login")
async def login(form_data: UserLogin):
    user = await User.find_one(User.email == form_data.email)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": str(user.id)})
    linkedin = await LinkedinConnect.find_one({"user_id": user.id})
    linkedin_access_token = None
    if linkedin:
       linkedin_access_token = linkedin.access_token
    return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user":user,
            "linkedin_access_token":linkedin_access_token,
            "is_linkedin_connected": user.is_linkedin_connected,
            "expires_in":linkedin.expires_in if linkedin else None
            }
