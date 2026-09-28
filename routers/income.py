from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId

from models.income_model import Income
from database.mongodb import income_collection
from utils.response import success_response

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


@router.post("/")
def create_income(income: Income):

    income_data = income.dict()

    result = income_collection.insert_one(income_data)

    return success_response(
        "Income created successfully",
        {
            "income_id": str(result.inserted_id)
        }
    )


@router.get("/")
def get_income():

    income_list = []

    for income in income_collection.find():

        income["_id"] = str(income["_id"])

        income_list.append(income)

    return success_response(
        "Income fetched successfully",
        income_list
    )


@router.get("/{income_id}")
def get_income_by_id(income_id: str):

    try:

        income = income_collection.find_one(
            {"_id": ObjectId(income_id)}
        )

        if not income:

            raise HTTPException(
                status_code=404,
                detail="Income not found"
            )

        income["_id"] = str(income["_id"])

        return success_response(
            "Income fetched successfully",
            income
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.put("/{income_id}")
def update_income(income_id: str, income: Income):

    try:

        income_data = income.dict()

        result = income_collection.update_one(
            {"_id": ObjectId(income_id)},
            {"$set": income_data}
        )

        if result.matched_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Income not found"
            )

        return success_response(
            "Income updated successfully",
            {
                "income_id": income_id
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.delete("/{income_id}")
def delete_income(income_id: str):

    try:

        result = income_collection.delete_one(
            {"_id": ObjectId(income_id)}
        )

        if result.deleted_count == 0:

            raise HTTPException(
                status_code=404,
                detail="Income not found"
            )

        return success_response(
            "Income deleted successfully",
            {
                "income_id": income_id
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    