from datetime import datetime
from typing import Optional, Literal, List
from bson import ObjectId
from beanie import Document

class Post(Document):
    user_id: ObjectId
    content: str
    content_type: Literal["text", "image", "video", "link", "post"] = "text"
    status: Literal["draft", "scheduled", "posted"] = "draft"
    platform: Literal["linkedin", "instagram", "twitter"] = "linkedin"
    schedule_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    # 🔹 New fields
    hashtags: Optional[List[str]] = []
    visibility: Literal["public", "private"] = "public"

    class Settings:
        name = "posts"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }
