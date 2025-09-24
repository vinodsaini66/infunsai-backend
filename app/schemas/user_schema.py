from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from bson import ObjectId
from beanie import PydanticObjectId

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    email: EmailStr
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True  # instead of orm_mode
        validate_by_name = True # instead of allow_population_by_field_name
        json_encoders = {ObjectId: str}


class UserAccountType(BaseModel):
    account_type: Literal["job-seeker", "influencer"]
