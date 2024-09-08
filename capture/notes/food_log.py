import csv
from itertools import islice

from pydantic import BaseModel


class FoodLog:
    def __init__(self, path: str):
        self.path = path

    def add_entries(self, entries: list[BaseModel]):
        with open(self.path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                writer.writerow(list(entry.model_dump().values()))

    def get_first_n_lines(self, n: int):
        with open(self.path, mode="r", newline="") as file:
            reader = csv.reader(file)
            lines = list(islice(reader, n))
        return lines
