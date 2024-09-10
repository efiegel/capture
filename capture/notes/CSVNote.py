import csv
from itertools import islice

from pydantic import BaseModel

from .BaseNote import BaseNote


class CSVNote(BaseNote[list[list[str]]]):
    def read(self) -> list[list[str]]:
        with open(self.file_path, newline="") as file:
            reader = csv.reader(file)
            return list(reader)

    def write(self, content: list[list[str]], append: bool = True):
        mode = "a" if append else "w"
        with open(self.file_path, mode, newline="") as file:
            writer = csv.writer(file)
            writer.writerows(content)

    def add_entries(self, entries: list[BaseModel]):
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                writer.writerow(list(entry.model_dump().values()))

    def write_headers(self, headers: list[str]):
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    def get_first_n_lines(self, n: int):
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            lines = list(islice(reader, n))
        return lines
