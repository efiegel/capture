import os
from pathlib import Path

from capture.llm import Agent
from capture.notes import BaseNote, CSVNote, TextNote


class NotesService:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory
        self.agent = Agent("gpt-4o-mini")

    def add_content_to_text_note(self, note: TextNote, content: str):
        existing_content = note.read()
        updated_content = self.agent.integrate(existing_content, content)
        note.write(updated_content)

    def add_content_to_csv_note(self, note: CSVNote, content: str):
        first_lines = note.read()[:5]
        schema = self.agent.infer_csv_schema(first_lines or content)
        entries = self.agent.parse(content, list[schema])
        if not first_lines:
            note.write([list(schema.model_fields.keys())])
        note.write([list(entry.model_dump().values()) for entry in entries])

    def _get_or_init_note(self, file_path: str) -> BaseNote:
        if not os.path.exists(file_path):
            Path(file_path).touch()
        if file_path.endswith(".csv"):
            return CSVNote(file_path)
        else:
            return TextNote(file_path)

    def add_content(self, content: str):
        file = self.agent.select_file(self.notes_directory, content)
        note = self._get_or_init_note(file)
        if isinstance(note, CSVNote):
            self.add_content_to_csv_note(note, content)
        else:
            self.add_content_to_text_note(note, content)
