from beanie import Document
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

class Post(Document):
    user_id: ObjectId
    content: str
    content_type: Literal["text", "image", "video", "link"]
    status: Literal["draft", "scheduled", "posted"] = "draft"
    platform: Literal["linkedin", "instagram","twitter"] = "linkedin"
    schedule_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "posts"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str   # ObjectId ko JSON response me string banado
        }
    }