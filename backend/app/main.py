from fastapi import FastAPI
from app.routers import auth, expense, food, exercise, focus
from mangum import Mangum
import os

# Get stage from environment variable, default to empty string for local development
stage = os.getenv("STAGE", "")
root_path = f"/{stage}" if stage else ""

app = FastAPI(root_path=root_path)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expense.router, prefix="/expense", tags=["expense"])
app.include_router(food.router, prefix="/food", tags=["food"])
app.include_router(exercise.router, prefix="/exercise", tags=["exercise"])
app.include_router(focus.router, prefix="/focus", tags=["focus"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to Everything Tracker API (Stage: {stage or 'local'})"}

# Lambda handler
handler = Mangum(app)