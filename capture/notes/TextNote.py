import os

from .BaseNote import BaseNote


class TextNote(BaseNote[str]):
    def read(self) -> str:
        if not os.path.exists(self.file_path):
            return ""

        with open(self.file_path, "r") as file:
            return file.read()

    def write(self, content: str):
        with open(self.file_path, "w") as file:
            file.write(content)
