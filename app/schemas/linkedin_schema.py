from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LinkedinConnectCreate(BaseModel):
    linkedin_id: str
    access_token: str
    refresh_token: Optional[str] = None 
    
