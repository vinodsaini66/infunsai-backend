from fastapi import FastAPI
from app.core.error_handlers import init_exception_handlers
from app.api.v1 import auth_routes, user_routes,linkedin_routes,post_routes
from app.middlewares.auth_middleware import AuthMiddleware
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.core.logging_config import setup_logging
import logging
from app.scheduler.post import start_post_scheduler

app = FastAPI(title="FastAPI + MongoDB + JWT",debug=True)
setup_logging()
logger = logging.getLogger(__name__)

# Middleware
app.add_middleware(AuthMiddleware)

# Routes
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])
app.include_router(linkedin_routes.router, prefix="/api/v1/linkedin", tags=["LinkedIn"])
app.include_router(post_routes.router, prefix="/api/v1/post", tags=["Post"])

# Global Error Handlers
init_exception_handlers(app)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()
    # start_post_scheduler()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()
