import csv
import os
from datetime import datetime

import pytest
import time_machine

from capture.notes.notes_service import NotesService
from tests.utils import patch_json_parsing, patch_model_responses


class TestNotesService:
    @pytest.fixture
    def daily_note_directory(self, tmp_path):
        dir = tmp_path / "daily_notes"
        dir.mkdir()
        return dir

    @pytest.fixture
    def daily_note(self, daily_note_directory):
        with time_machine.travel(datetime(1985, 10, 26)):
            file = f"{daily_note_directory}/{datetime.now().strftime('%Y-%m-%d')}.md"
            with open(file, "w") as f:
                f.write("This is a sample note.")
            yield file

    @pytest.fixture
    def food_log(self, tmp_path):
        file = f"{tmp_path}/food_log.csv"

        with open(file, "w") as f:
            csv.writer(f).writerow(
                [
                    "time",
                    "name",
                    "qty",
                    "unit",
                    "calories",
                    "protein_grams",
                    "fat_grams",
                    "carbs_grams",
                    "sodium_mg",
                ]
            )
            csv.writer(f).writerow(
                ["1985-10-26 9:00", "pear", 1, "whole", 100.0, 0.5, 0.3, 22.0, 2.0]
            )

        yield file

    @time_machine.travel(datetime(1985, 10, 26))
    @pytest.mark.usefixtures("daily_note_directory")
    def test_add_content_creates_new_daily_note(self, tmp_path):
        daily_note = f"{tmp_path}/daily_notes/{datetime.now().strftime('%Y-%m-%d')}.md"
        assert os.path.exists(daily_note) is False

        notes_service = NotesService(tmp_path)
        integrated_content = "This is a sample note.\n\nMore content!"
        with patch_model_responses([daily_note, integrated_content]):
            notes_service.add_content("New content for a new note!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content

    @time_machine.travel(datetime(1985, 10, 26))
    def test_add_content_writes_to_existing_daily_note(self, tmp_path, daily_note):
        notes_service = NotesService(tmp_path)
        integrated_content = "This is a sample note.\n\nMore content!"
        with patch_model_responses([daily_note, integrated_content]):
            notes_service.add_content("More content!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content

    def test_add_content_writes_to_food_log(self, tmp_path, food_log):
        notes_service = NotesService(tmp_path)
        entry_list = [
            {
                "time": "12:00",
                "name": "apple",
                "qty": 1,
                "unit": "whole",
                "calories": 95.0,
                "protein_grams": 0.5,
                "fat_grams": 0.3,
                "carbs_grams": 25.0,
                "sodium_mg": 2.0,
            }
        ]

        schema_str = (
            "time: str, name: str, qty: float, unit: str, calories: float, protein_gr"
            "ams: float, fat_grams: float, carbs_grams: float, sodium_mg: float"
        )

        # need to patch the model call that parses the food log entries so that the api
        # isn't actually called, but also patching the parsed result which is the actual
        # end of the chain; hence the None model response patch. Could wrap the chain
        # and mock the entire thing if desired, this is all a product of the | syntax.
        with patch_model_responses([food_log, schema_str, None]):
            with patch_json_parsing({"items": entry_list}):
                notes_service.add_content("I ate an apple at lunch.")

        with open(food_log, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            entries = [row for row in reader]

        assert entries[1] == (
            ["12:00", "apple", "1.0", "whole", "95.0", "0.5", "0.3", "25.0", "2.0"]
        )

    def test_add_content_writes_to_new_log(self, tmp_path):
        notes_service = NotesService(tmp_path)

        new_file_path = f"{tmp_path}/sleep_log.csv"
        schema_str = "asleep: str, awake: str"
        entry_list = [{"asleep": "2024-01-01 22:00", "awake": "2024-01-02 06:00"}]

        with patch_model_responses([new_file_path, schema_str, None]):
            with patch_json_parsing({"items": entry_list}):
                notes_service.add_content(
                    "New sleep log! Went to bed at 10pm and woke up at 6am."
                )

        with open(new_file_path, mode="r", newline="") as f:
            reader = csv.reader(f)
            entries = [row for row in reader]

        assert entries == [
            ["asleep", "awake"],
            ["2024-01-01 22:00", "2024-01-02 06:00"],
        ]
