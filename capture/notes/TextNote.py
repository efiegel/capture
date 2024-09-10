from .BaseNote import BaseNote


class TextNote(BaseNote[str]):
    def read(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def write(self, content: str):
        with open(self.file_path, "w") as file:
            file.write(content)
