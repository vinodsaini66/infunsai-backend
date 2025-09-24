from beanie import Document
from pydantic import EmailStr
from typing import Optional,Literal
from datetime import datetime


class User(Document):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    profile: Optional[str] = None
    is_linkedin_connected: bool = False  # ✅ boolean field
    account_type: Literal["job-seeker","influencer"] = "job-seeker"
    role: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"  # MongoDB collection name

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "hashedpassword123",
                "full_name": "John Doe"
            }
        }
