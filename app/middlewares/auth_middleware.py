from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/api/v1/auth/login","/api/v1/auth/signup", "/openapi.json", "/docs", "/redoc"]:
            return await call_next(request)

        token = request.headers.get("Authorization")
        
        if not token or not token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Missing or invalid token"
                }
            )

        token_data = verify_token(token.split(" ")[1])
        if not token_data: 
             return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Invalid or expired token"
                }
            )
            
        request.state.user = token_data
        return await call_next(request)
