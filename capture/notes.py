import csv
import json
import os
from datetime import datetime
from enum import Enum

from dotenv import load_dotenv

from capture.generator import Generator

load_dotenv()


class NoteType(str, Enum):
    DAILY = "daily"
    FOOD_LOG = "food_log"
    OTHER = "other"


class Notes:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory
        self.content_generator = Generator()

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

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)

    def add_content_to_daily_note(self, content: str):
        daily_note = self.get_or_create_daily_note()
        self.update_note(daily_note, content)

    def add_content_to_food_log(self, content: str):
        # TODO: decouple log from csv dependency
        food_log_path = os.path.expanduser(
            os.path.join(self.notes_directory, os.getenv("FOOD_LOG_PATH"))
        )
        parsed_entries = self.content_generator.parse_food_log_entries(content)
        entries = json.loads(parsed_entries).get("entries", [])  # TODO: fix output
        with open(food_log_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                entry["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow(list(entry.values()))

    def get_note_type(self, content: str) -> NoteType:
        return self.content_generator.choose_category(
            content, [NoteType.FOOD_LOG, NoteType.OTHER]
        )

    def add_content(self, text_file_path: str):
        with open(text_file_path, "r") as f:
            content = f.read()

        match self.get_note_type(content):
            case NoteType.DAILY:
                self.add_content_to_daily_note(content)
            case NoteType.FOOD_LOG:
                self.add_content_to_food_log(content)
            case _:
                self.add_content_to_daily_note(content)
