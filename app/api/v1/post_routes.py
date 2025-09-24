from fastapi import APIRouter, Depends, HTTPException, Query,Request,Body
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.models.post_model  import Post
from app.schemas.post_schema import PostCreate, PostOut
from collections import defaultdict
from typing import Dict, List
router = APIRouter()

# Create Post
@router.post("/", response_model=PostOut)
async def create_post(data: PostCreate, request: Request):
    user=request.state.user 
    post = Post(
        user_id=ObjectId(user["sub"]),
        content=data.content,
        content_type=data.content_type,
        status=data.status,
        schedule_at=data.schedule_at
    )
    await post.insert()
    return PostOut(
        id=str(post.id),
        content=post.content,
        content_type=post.content_type,
        status=post.status,
        schedule_at=post.schedule_at,
        posted_at=post.posted_at,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )

@router.get("/scheduled")
async def get_scheduled_posts(request: Request):
    user=request.state.user 
    print(user)
    posts = await Post.find(
        {
            "user_id": ObjectId(user["sub"]),
            "status": "scheduled"
        }
    ).sort("+schedule_at").to_list()

    grouped_posts: Dict[str, List[PostOut]] = defaultdict(list)

    for post in posts:
        if post.schedule_at:
            print("start")
            date_key = post.schedule_at.date().isoformat()  # "YYYY-MM-DD"
            grouped_posts[date_key].append(
                PostOut(
                    id=str(post.id),
                    content=post.content,
                    content_type=post.content_type,
                    status=post.status,
                    schedule_at=post.schedule_at,
                    posted_at=post.posted_at,
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
            )

    return grouped_posts

# Get All Posts (with filter + sort)
@router.get("/", response_model=List[PostOut])
async def get_posts(
     request: Request,
    status: Optional[str] = Query(None, description="Filter by status"),
    sort: Optional[str] = Query("desc", description="Sort by posted_at asc/desc"),
):
    user=request.state.user 
    query = Post.find(Post.user_id == ObjectId(user["sub"]))
    if status:
        query = query.find(Post.status == status)

    if sort == "asc":
        query = query.sort("+posted_at")
    else:
        query = query.sort("-posted_at")

    posts = await query.to_list()
    return [
        PostOut(
            id=str(post.id),
            content=post.content,
            content_type=post.content_type,
            status=post.status,
            schedule_at=post.schedule_at,
            posted_at=post.posted_at,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        for post in posts
    ]

# Get Post Detail
@router.get("/{post_id}", response_model=PostOut)
async def get_post_detail(post_id: str, request: Request):
    user=request.state.user 
    post = await Post.find_one({"_id": ObjectId(post_id), "user_id": ObjectId(user["sub"])})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostOut(
        id=str(post.id),
        content=post.content,
        content_type=post.content_type,
        status=post.status,
        schedule_at=post.schedule_at,
        posted_at=post.posted_at,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


# Update Post
@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    request: Request,
    post_id: str,
    data: PostCreate = Body(...),
):
    user=request.state.user 
    post = await Post.find_one({"_id": ObjectId(post_id), "user_id": ObjectId(user["sub"])})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.content = data.content
    post.content_type = data.content_type
    post.status = data.status
    post.schedule_at = data.schedule_at
    post.updated_at = datetime.now()

    if data.status == "posted" and not post.posted_at:
        post.posted_at = datetime.now()

    await post.save()

    return PostOut(
        id=str(post.id),
        content=post.content,
        content_type=post.content_type,
        status=post.status,
        schedule_at=post.schedule_at,
        posted_at=post.posted_at,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


# Delete Post
@router.delete("/{post_id}")
async def delete_post(post_id: str,request: Request,):
    user=request.state.user
    post = await Post.find_one({"_id": ObjectId(post_id), "user_id": ObjectId(user["sub"])})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await post.delete()
    return {"message": "Post deleted successfully", "id": post_id}
