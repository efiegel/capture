import csv

from pydantic import BaseModel


class FoodLogEntry(BaseModel):
    time: str
    name: str
    qty: float
    unit: str


class FoodLog:
    def __init__(self, path: str):
        self.path = path

    def add_entries(self, entries: list[FoodLogEntry]):
        with open(self.path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                writer.writerow(list(entry.values()))
