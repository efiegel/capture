import os
from datetime import datetime


class Notes:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory

    def get_or_create_daily_note(self) -> str:
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        file_path = f"{self.notes_directory}/{file_name}"
        if not os.path.exists(file_path):
            self.write("", file_path)
        return file_path

    def update_note(self, file_path, content):
        pass

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)

    def add_content(self, text_file_path: str):
        with open(text_file_path, "r") as f:
            content = f.read()

        file_name = os.path.basename(text_file_path)
        note_file_name = file_name.replace(".txt", ".md")
        note_path = f"{self.notes_directory}/{note_file_name}"
        self.write(content, note_path)
