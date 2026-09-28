from pydantic import BaseModel
from datetime import date


class Expense(BaseModel):

    title: str
    amount: float
    category: str
    date: date
    description: str
    user_id: str