import os
from datetime import datetime
from pathlib import Path

from capture.llm import Agent
from capture.notes.CSVNote import CSVNote


class NotesService:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory
        self.agent = Agent("gpt-4o-mini")

    def get_or_create_daily_note(self) -> str:
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        file_path = os.path.join(self.notes_directory, "daily_notes", file_name)
        if not os.path.exists(file_path):
            self.write("", file_path)
        return file_path

    def update_note(self, file_path, new_content):
        with open(file_path, "r") as f:
            existing_content = f.read()

        updated_content = self.agent.integrate(existing_content, new_content)
        self.write(updated_content, file_path)

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)

    def add_content_to_daily_note(self, content: str):
        daily_note = self.get_or_create_daily_note()
        self.update_note(daily_note, content)

    def add_content_to_csv_note(self, file_path: str, content: str):
        note = CSVNote(file_path)
        csv_data = note.get_first_n_lines(5) or content
        schema = self.agent.infer_csv_schema(csv_data)
        entries = self.agent.parse(content, list[schema])
        note.add_entries(entries)

    def add_content(self, content: str):
        file = self.agent.select_file(self.notes_directory, content)
        if not os.path.exists(file):
            Path(file).touch()

        if file.endswith(".csv"):
            self.add_content_to_csv_note(file, content)
        else:
            self.add_content_to_daily_note(content)
