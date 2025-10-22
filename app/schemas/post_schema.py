from pydantic import BaseModel
from typing import Optional, Literal,List
from datetime import datetime

class PostCreate(BaseModel):
    content: str
    content_type: Literal["text", "image", "video", "link", "post"]
    status: Literal["draft", "scheduled", "posted"] = "draft"
    schedule_at: Optional[datetime] = None
    hashtags: Optional[List[str]] = []
    visibility: Literal["public", "private"] = "public"

class PostOut(BaseModel):
    id: str
    content: str
    content_type: str
    status: str
    schedule_at: Optional[datetime]
    posted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
