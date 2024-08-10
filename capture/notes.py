import os


class Notes:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory

    def create_from_text_file(self, text_file_path: str):
        with open(text_file_path, "r") as f:
            content = f.read()

        file_name = os.path.basename(text_file_path)
        note_file_name = file_name.replace(".txt", ".md")
        note_path = f"{self.notes_directory}/{note_file_name}"
        self.write(content, note_path)

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)
