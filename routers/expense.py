from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId

from models.expense_model import Expense
from database.mongodb import expense_collection
from utils.response import success_response

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


# CREATE EXPENSE
@router.post("/")
def create_expense(expense: Expense):

    expense_data = expense.dict()

    result = expense_collection.insert_one(expense_data)

    return success_response(
        "Expense created successfully",
        {
            "expense_id": str(result.inserted_id)
        }
    )


# GET ALL EXPENSES
@router.get("/")
def get_expenses():

    expenses = []

    for expense in expense_collection.find():

        expense["_id"] = str(expense["_id"])

        expenses.append(expense)

    return success_response(
        "Expenses fetched successfully",
        expenses
    )


# GET EXPENSE BY ID
@router.get("/{expense_id}")
def get_expense(expense_id: str):

    try:

        expense = expense_collection.find_one(
            {"_id": ObjectId(expense_id)}
        )

        if not expense:

            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        expense["_id"] = str(expense["_id"])

        return success_response(
            "Expense fetched successfully",
            expense
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid Expense ID"
        )


# UPDATE EXPENSE
@router.put("/{expense_id}")
def update_expense(
    expense_id: str,
    expense: Expense
):

    try:

        expense_data = expense.dict()

        result = expense_collection.update_one(
            {"_id": ObjectId(expense_id)},
            {"$set": expense_data}
        )

        if result.matched_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return success_response(
            "Expense updated successfully"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid Expense ID"
        )


# DELETE EXPENSE
@router.delete("/{expense_id}")
def delete_expense(expense_id: str):

    try:

        result = expense_collection.delete_one(
            {"_id": ObjectId(expense_id)}
        )

        if result.deleted_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return success_response(
            "Expense deleted successfully"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid Expense ID"
        )
    


from database.mongodb import expense_collection, income_collection


@router.get("/summary")
def expense_summary():

    total_expense = 0
    total_income = 0

    for expense in expense_collection.find():
        total_expense += expense["amount"]

    for income in income_collection.find():
        total_income += income["amount"]

    balance = total_income - total_expense

    return success_response(
        "Summary fetched successfully",
        {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        }
    )



@router.get("/category/{category}")
def get_expense_by_category(category: str):

    expense_list = []

    for expense in expense_collection.find(
        {"category": category}
    ):

        expense["_id"] = str(expense["_id"])

        expense_list.append(expense)

    return success_response(
        "Expenses fetched successfully",
        expense_list
    )