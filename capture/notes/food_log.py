import csv
from itertools import islice

from pydantic import BaseModel


class FoodLogEntry(BaseModel):
    time: str
    name: str
    qty: float
    unit: str
    calories: float
    protein_grams: float
    fat_grams: float
    carbs_grams: float
    sodium_mg: float


class FoodLog:
    def __init__(self, path: str):
        self.path = path

    def add_entries(self, entries: list[FoodLogEntry]):
        with open(self.path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                writer.writerow(list(entry.model_dump().values()))

    def get_first_n_lines(self, n: int):
        with open(self.path, mode="r", newline="") as file:
            reader = csv.reader(file)
            lines = list(islice(reader, n))
        return lines
