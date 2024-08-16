import os
from datetime import datetime
from unittest.mock import patch

import pytest
import time_machine

from capture.notes.notes_service import NotesService


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
    def test_add_content_creates_new_daily_note(self, tmp_path, daily_note_directory):
        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")
        daily_note = f"{tmp_path}/daily_notes/{datetime.now().strftime('%Y-%m-%d')}.md"
        assert os.path.exists(daily_note) is False

        new_content = "New content for a new note!"
        with patch.object(notes_service.content_generator, "integrate_content") as mock:
            mock.return_value = new_content
            notes_service.add_content_to_daily_note(new_content)

        daily_note = f"{tmp_path}/daily_notes/{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(daily_note, "r") as f:
            content = f.read()

        assert content == new_content

    @time_machine.travel(datetime(1985, 10, 26))
    def test_add_content_writes_to_existing_daily_note(self, tmp_path, daily_note):
        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")

        new_content = "Here's some more content!"
        integrated_content = "This is a sample note.\n\nHere's some more content!"
        with patch.object(notes_service.content_generator, "integrate_content") as mock:
            mock.return_value = integrated_content
            notes_service.add_content_to_daily_note(new_content)

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content
