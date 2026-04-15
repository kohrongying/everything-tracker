import os
import uuid
from datetime import datetime, UTC

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers import auth, expense, food, exercise, focus
from app.core.config import settings

logger = Logger(service="everything-tracker")

# Get stage from environment variable, default to empty string for local development
stage = os.getenv("STAGE", "")
root_path = f"/{stage}" if stage else ""

app = FastAPI(root_path=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = (
            request.headers.get("x-correlation-id")
            or request.headers.get("X-Amzn-Trace-Id")
            or str(uuid.uuid4())
        )
        logger.append_keys(correlation_id=correlation_id)

        start_time = datetime.now(UTC)
        response = None
        try:
            logger.info(
                "Incoming request",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "client_ip": request.client.host if request.client else None,
                }
            )
            response = await call_next(request)
            process_time = (datetime.now(UTC) - start_time).total_seconds()
            response.headers["X-Correlation-Id"] = correlation_id

            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time": process_time,
                }
            )
            return response
        except Exception as e:
            process_time = (datetime.now(UTC) - start_time).total_seconds()
            logger.exception(
                "Request failed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "process_time": process_time,
                    "error": str(e),
                }
            )
            raise
        finally:
            logger.remove_keys(["correlation_id"])

app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expense.router, prefix="/expense", tags=["expense"])
app.include_router(food.router, prefix="/food", tags=["food"])
app.include_router(exercise.router, prefix="/exercise", tags=["exercise"])
app.include_router(focus.router, prefix="/focus", tags=["focus"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": f"Welcome to Everything Tracker API (Stage: {stage or 'local'})"}

# Log application startup
logger.info(
    "Application started",
    extra={
        "stage": stage or "local",
        "root_path": root_path,
        "environment": "lambda" if os.getenv("AWS_LAMBDA_FUNCTION_NAME") else "local",
    }
)

# Lambda handler
_mangum_handler = Mangum(app)

@logger.inject_lambda_context
def handler(event, context: LambdaContext):
    return _mangum_handler(event, context)