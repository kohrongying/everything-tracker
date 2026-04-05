from fastapi import FastAPI
from app.routers import auth, expense, food, exercise, focus
from mangum import Mangum

app = FastAPI(title="Everything Tracker API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(expense.router, prefix="/expense", tags=["expense"])
app.include_router(food.router, prefix="/food", tags=["food"])
app.include_router(exercise.router, prefix="/exercise", tags=["exercise"])
app.include_router(focus.router, prefix="/focus", tags=["focus"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Everything Tracker API"}

# Lambda handler
handler = Mangum(app)