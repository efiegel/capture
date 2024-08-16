import os

import pytest

from capture.notes.notes_service import NotesService


class TestNotesService:
    @pytest.fixture
    def daily_note(self):
        file = "tests/sample_data/daily_notes/2024-08-16.md"
        with open(file, "w") as f:
            f.write("This is a sample note.")
        yield file
        os.remove(file)

    def test_add_daily_note_content(self, daily_note):
        notes_service = NotesService("tests/sample_data/", "tests/sample_data/food.csv")

        new_content = "Here's some more content!"
        notes_service.add_content_to_daily_note(new_content)

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == "This is a sample note.\n\nHere's some more content!"
