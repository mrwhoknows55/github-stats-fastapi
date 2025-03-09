from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.models.github import ErrorResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    handler for HTTPException, returns a standardized error format.
    """
    error_response = ErrorResponse(
        error=exc.detail,
        code=exc.status_code
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )
