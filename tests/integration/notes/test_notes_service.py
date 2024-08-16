import os
from datetime import datetime
from unittest.mock import patch

import pytest
import time_machine

from capture.notes.notes_service import NotesService

CHOOSE_CATEGORY = "capture.notes.content_generator.ContentGenerator.choose_category"
INTEGRATE_CONTENT = "capture.notes.content_generator.ContentGenerator.integrate_content"


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
