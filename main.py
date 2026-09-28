from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.expense import router as expense_router
from routers.income import router as income_router
from routers.dashboard import router as dashboard_router

app = FastAPI(
    title="Expense Tracker API"
)

app.include_router(auth_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(dashboard_router)
@app.get("/")
def home():
    return {
        "message": "Expense Tracker API Running"
    }