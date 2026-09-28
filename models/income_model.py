from pydantic import BaseModel
from datetime import date


class Income(BaseModel):

    title: str
    amount: float
    source: str
    date: date
    description: str
    user_id: str