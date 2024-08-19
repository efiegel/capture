import csv
import json
import os
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import time_machine

from capture.notes.notes_service import NotesService


def mock_chat_completions(client, method, return_content, beta=False):
    response = MagicMock()
    response.choices[0].message.content = return_content

    if beta:
        return patch.object(
            client.beta.chat.completions,
            method,
            return_value=response,
        )
    else:
        return patch.object(
            client.chat.completions,
            method,
            return_value=response,
        )


def patch_model_response(return_content):
    return patch(
        "langchain_openai.ChatOpenAI.invoke",
        return_value=MagicMock(content=return_content),
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
        openai_client = notes_service.content_generator.client
        integrated_content = "This is a sample note.\n\nMore content!"

        with mock_chat_completions(openai_client, "create", "daily_note"):
            with mock_chat_completions(openai_client, "create", integrated_content):
                notes_service.add_content("New content for a new note!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content

    @time_machine.travel(datetime(1985, 10, 26))
    def test_add_content_writes_to_existing_daily_note(self, tmp_path, daily_note):
        notes_service = NotesService(tmp_path, "tests/sample_data/food.csv")

        openai_client = notes_service.content_generator.client
        integrated_content = "This is a sample note.\n\nMore content!"

        with mock_chat_completions(openai_client, "create", "daily_note"):
            with mock_chat_completions(openai_client, "create", integrated_content):
                notes_service.add_content("More content!")

        with open(daily_note, "r") as f:
            content = f.read()

        assert content == integrated_content

    def test_add_content_writes_to_food_log(self, tmp_path, food_log):
        notes_service = NotesService(tmp_path, food_log)

        openai_client = notes_service.content_generator.client
        entry_list = [{"time": "12:00", "name": "apple", "qty": 1, "unit": "whole"}]
        entries = json.dumps({"entries": entry_list})

        with patch_model_response("food_log"):
            with mock_chat_completions(openai_client, "parse", entries, beta=True):
                notes_service.add_content("I ate an apple at lunch.")

        with open(food_log, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            entries = [row for row in reader]

        assert entries == [["12:00", "apple", "1", "whole"]]
