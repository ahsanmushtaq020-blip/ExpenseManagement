from fastapi import APIRouter

from database.mongodb import (
    income_collection,
    expense_collection
)

from utils.response import success_response

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def dashboard():

    total_income = 0

    total_expense = 0

    for income in income_collection.find():

        total_income += income["amount"]

    for expense in expense_collection.find():

        total_expense += expense["amount"]

    balance = total_income - total_expense

    return success_response(
        "Dashboard fetched successfully",
        {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        }
    )