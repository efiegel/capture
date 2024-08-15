from pydantic import BaseModel


class FoodLogEntry(BaseModel):
    time: str
    name: str
    qty: float
    unit: str


class FoodLogEntries(BaseModel):
    entries: list[FoodLogEntry]
