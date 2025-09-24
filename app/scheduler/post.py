from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone
from app.models.post_model import Post
from bson import ObjectId

scheduler = AsyncIOScheduler()

async def process_scheduled_posts():
    now = datetime.now(timezone.utc)
    posts = await Post.find({
        "status": "scheduled",
        "schedule_at": {"$lte": now}
    }).to_list()

    for post in posts:
        post.status = "posted"
        post.posted_at = now
        post.updated_at = now
        await post.save()
        print(f"✅ Post {post.id} published at {now}")

def start_post_scheduler():
    scheduler.add_job(
        process_scheduled_posts,
        IntervalTrigger(seconds=30),   # har 30 sec me check karega
        id="process_scheduled_posts",
        replace_existing=True,
    )
    scheduler.start()
