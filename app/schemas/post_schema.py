from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class PostCreate(BaseModel):
    content: str
    content_type: Literal["text", "image", "video", "link"]
    status: Literal["draft", "scheduled", "posted"] = "draft"
    schedule_at: Optional[datetime] = None

class PostOut(BaseModel):
    id: str
    content: str
    content_type: str
    status: str
    schedule_at: Optional[datetime]
    posted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
