import json
import os
from datetime import datetime
from enum import Enum

from capture.db import Note, database_context
from capture.notes.content_generator import ContentGenerator
from capture.notes.food_log import FoodLog


class NoteType(str, Enum):
    DAILY = "daily"
    FOOD_LOG = "food_log"
    OTHER = "other"


class NotesService:
    def __init__(self, notes_directory: str, food_log_path: str) -> None:
        self.notes_directory = notes_directory
        self.food_log_path = food_log_path
        self.content_generator = ContentGenerator()

    def get_or_create_daily_note(self) -> str:
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        file_path = os.path.join(self.notes_directory, "daily_notes", file_name)
        if not os.path.exists(file_path):
            self.write("", file_path)
        return file_path

    def update_note(self, file_path, new_content):
        with open(file_path, "r") as f:
            existing_content = f.read()

        updated_content = self.content_generator.integrate_content(
            existing_content, new_content
        )
        self.write(updated_content, file_path)

        return updated_content

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)

    def add_content_to_daily_note(self, content: str):
        daily_note = self.get_or_create_daily_note()
        return self.update_note(daily_note, content)

    def add_content_to_food_log(self, content: str):
        entries = self.content_generator.parse_food_log_entries(content)
        log = FoodLog(self.food_log_path)
        log.add_entries(entries)
        return entries

    def get_note_type(self, content: str) -> NoteType:
        return self.content_generator.choose_category(
            content, [NoteType.FOOD_LOG, NoteType.OTHER]
        )

    def add_content(self, content: str):
        note_type = self.get_note_type(content)
        match note_type:
            case NoteType.FOOD_LOG:
                parsed_data = self.add_content_to_food_log(content)
                data = json.dumps([item.model_dump() for item in parsed_data])
            case _:
                data = self.add_content_to_daily_note(content)

        with database_context():
            note = Note.create(type=note_type, raw_text=content, parsed_data=data)
            note.save()
