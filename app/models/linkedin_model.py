from beanie import Document
from typing import Optional
from datetime import datetime
from bson import ObjectId


class LinkedinConnect(Document):
    user_id: ObjectId   # reference to User._id
    linkedin_id: str
    access_token: str
    refresh_token: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    class Settings:
        name = "linkedin_connects"  # MongoDB collection name
        
        
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str   # ObjectId ko JSON response me string banado
        }
    }

   