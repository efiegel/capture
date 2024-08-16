import csv
import os
from datetime import datetime
from unittest.mock import patch

import pytest
import time_machine

from capture.notes.notes_service import NotesService

CONTENT_GENERATOR = "capture.notes.content_generator.ContentGenerator"
CHOOSE_CATEGORY = f"{CONTENT_GENERATOR}.choose_category"
INTEGRATE_CONTENT = f"{CONTENT_GENERATOR}.integrate_content"
PARSE_FOOD_LOG_ENTRIES = f"{CONTENT_GENERATOR}.parse_food_log_entries"


class TestNotesService:
    @pytest.fixture
    def daily_note_directory(self, tmp_path):
        d = tmp_path / "daily_notes"
        d.mkdir()
        return d

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
            csv.writer(f).writerow(["time", "name", "qty", "unit"])
        yield file

    @time_machine.travel(datetime(1985, 10, 26))
    @pytest.mark.usefixtures("daily_note_directory")
    @patch(INTEGRATE_CONTENT, return_value="New content for a new note!")
    @patch(CHOOSE_CATEGORY, return_value="daily")
    def test_add_content_creates_new_daily_note(self, _, integrated_content, tmp_path):
        daily_note = f"{tmp_path}/daily_notes/{datetime.now().strftime('%Y-%m-%d')}.md"
        assert os.path.exists(daily_note) is False

        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")
        notes_service.add_content("New content for a new note!")
        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content.return_value

    @time_machine.travel(datetime(1985, 10, 26))
    @patch(INTEGRATE_CONTENT, return_value="This is a sample note.\n\nMore content!")
    @patch(CHOOSE_CATEGORY, return_value="daily")
    def test_add_content_writes_to_existing_daily_note(
        self, _, integrated_content, tmp_path, daily_note
    ):
        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")
        notes_service.add_content("More content!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content.return_value

    @patch(
        PARSE_FOOD_LOG_ENTRIES,
        return_value=[{"time": "12:00", "name": "apple", "qty": 1, "unit": "whole"}],
    )
    @patch(CHOOSE_CATEGORY, return_value="food_log")
    def test_add_content_writes_to_food_log(self, _, __, tmp_path, food_log):
        notes_service = NotesService(tmp_path, food_log)
        notes_service.add_content("I ate an apple at lunch.")

        with open(food_log, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            entries = [row for row in reader]

        assert entries == [["12:00", "apple", "1", "whole"]]
