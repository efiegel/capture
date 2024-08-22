import csv
import os
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import time_machine
from langchain_core.messages import BaseMessage

from capture.notes.notes_service import NotesService


def patch_model_responses(responses):
    return patch(
        "langchain_openai.ChatOpenAI.invoke",
        side_effect=[
            MagicMock(spec=BaseMessage, content=response, text=str(response))
            for response in responses
        ],
    )


def patch_json_parsing(result):
    return patch(
        "langchain_core.output_parsers.json.JsonOutputParser.parse_result",
        side_effect=[result],
    )


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
            csv.writer(f).writerow(["time", "name", "qty", "unit"])
        yield file

    @time_machine.travel(datetime(1985, 10, 26))
    @pytest.mark.usefixtures("daily_note_directory")
    def test_add_content_creates_new_daily_note(self, tmp_path):
        daily_note = f"{tmp_path}/daily_notes/{datetime.now().strftime('%Y-%m-%d')}.md"
        assert os.path.exists(daily_note) is False

        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")
        integrated_content = "This is a sample note.\n\nMore content!"
        with patch_model_responses(["daily_note", integrated_content]):
            notes_service.add_content("New content for a new note!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content

    @time_machine.travel(datetime(1985, 10, 26))
    def test_add_content_writes_to_existing_daily_note(self, tmp_path, daily_note):
        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")
        integrated_content = "This is a sample note.\n\nMore content!"
        with patch_model_responses(["daily_note", integrated_content]):
            notes_service.add_content("More content!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content

    def test_add_content_writes_to_food_log(self, tmp_path, food_log):
        notes_service = NotesService(tmp_path, food_log)
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

        # need to patch the model call that parses the food log entries so that the api
        # isn't actually called, but also patching the parsed result which is the actual
        # end of the chain; hence the None model response patch. Could wrap the chain
        # and mock the entire thing if desired, this is all a product of the | syntax.
        with patch_model_responses(["food_log", None]):
            with patch_json_parsing({"entries": entry_list}):
                notes_service.add_content("I ate an apple at lunch.")

        with open(food_log, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            entries = [row for row in reader]

        assert entries == [
            ["12:00", "apple", "1.0", "whole", "95.0", "0.5", "0.3", "25.0", "2.0"]
        ]
