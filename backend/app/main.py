import logging
import sys
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import auth, expense, food, exercise, focus
from mangum import Mangum
import os
import json
from datetime import datetime, UTC

# Configure logging for AWS CloudWatch
class CloudWatchFormatter(logging.Formatter):
    """Custom formatter for AWS CloudWatch structured logging."""

    def format(self, record):
        # Add timestamp in ISO format
        record.timestamp = datetime.now(UTC).isoformat()

        # Add stage information
        record.stage = os.getenv("STAGE", "local")

        # Create structured log entry
        log_entry = {
            "timestamp": record.timestamp,
            "level": record.levelname,
            "stage": record.stage,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if they exist
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create console handler with CloudWatch formatter
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(CloudWatchFormatter())
logger.addHandler(console_handler)

# Create application logger
app_logger = logging.getLogger("everything-tracker")

# Get stage from environment variable, default to empty string for local development
stage = os.getenv("STAGE", "")
root_path = f"/{stage}" if stage else ""

app = FastAPI(root_path=root_path)

# Custom middleware for request logging
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now(UTC)

        # Log incoming request
        app_logger.info(
            "Incoming request",
            extra={
                "extra_fields": {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "client_ip": request.client.host if request.client else None,
                }
            }
        )

        try:
            response = await call_next(request)
            process_time = (datetime.now(UTC) - start_time).total_seconds()

            # Log successful response
            app_logger.info(
                "Request completed",
                extra={
                    "extra_fields": {
                        "method": request.method,
                        "url": str(request.url),
                        "status_code": response.status_code,
                        "process_time": process_time,
                    }
                }
            )

            return response

        except Exception as e:
            process_time = (datetime.now(UTC) - start_time).total_seconds()

            # Log error response
            app_logger.error(
                "Request failed",
                exc_info=True,
                extra={
                    "extra_fields": {
                        "method": request.method,
                        "url": str(request.url),
                        "process_time": process_time,
                        "error": str(e),
                    }
                }
            )
            raise

# Add middleware
app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expense.router, prefix="/expense", tags=["expense"])
app.include_router(food.router, prefix="/food", tags=["food"])
app.include_router(exercise.router, prefix="/exercise", tags=["exercise"])
app.include_router(focus.router, prefix="/focus", tags=["focus"])

@app.get("/")
def read_root():
    app_logger.info("Root endpoint accessed")
    return {"message": f"Welcome to Everything Tracker API (Stage: {stage or 'local'})"}

# Log application startup
app_logger.info(
    "Application started",
    extra={
        "extra_fields": {
            "stage": stage or "local",
            "root_path": root_path,
            "environment": "lambda" if os.getenv("AWS_LAMBDA_FUNCTION_NAME") else "local",
        }
    }
)

# Lambda handler
handler = Mangum(app)