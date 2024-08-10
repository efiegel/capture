import os
from datetime import datetime

from capture.generator import Generator


class Notes:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory

    def get_or_create_daily_note(self) -> str:
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        file_path = f"{self.notes_directory}/{file_name}"
        if not os.path.exists(file_path):
            self.write("", file_path)
        return file_path

    def update_note(self, file_path, new_content):
        with open(file_path, "r") as f:
            existing_content = f.read()

        content_generator = Generator()
        updated_content = content_generator.integrate_content(
            existing_content, new_content
        )
        self.write(updated_content, file_path)

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)

    def add_content(self, text_file_path: str):
        with open(text_file_path, "r") as f:
            content = f.read()

        daily_note = self.get_or_create_daily_note()
        self.update_note(daily_note, content)
