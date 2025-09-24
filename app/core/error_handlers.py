from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback


def init_exception_handlers(app):
    # Handle HTTPException (like 401, 404, etc.)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "code": exc.status_code,
                "path": request.url.path,
            },
        )

    # Handle Validation Errors (from Pydantic or FastAPI request body)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation error",
                "errors": exc.errors(),
                "body": exc.body,
                "code": 422,
                "path": request.url.path,
            },
        )

    # Handle unexpected exceptions (like 500s)
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Internal server error",
                "detail": str(exc),   # ⚠️ remove in production if you don’t want to expose details
                "code": 500,
                "path": request.url.path,
                "trace": traceback.format_exc().splitlines()[-3:],  # last 3 lines of stacktrace
            },
        )
