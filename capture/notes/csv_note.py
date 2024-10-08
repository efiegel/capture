import csv
import os

from .base_note import BaseNote


class CSVNote(BaseNote[list[list[str]]]):
    def read(self) -> list[list[str]]:
        if not os.path.exists(self.file_path):
            return [[]]

        with open(self.file_path, newline="") as file:
            reader = csv.reader(file)
            return list(reader)

    def write(self, content: list[list[str]], append: bool = True):
        mode = "a" if append else "w"
        with open(self.file_path, mode, newline="") as file:
            writer = csv.writer(file)
            writer.writerows(content)
