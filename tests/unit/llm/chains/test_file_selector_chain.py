import csv

import pytest
from langchain_openai import ChatOpenAI

from capture.llm.chains import FileSelectorChain
from tests.utils import patch_model_responses


class TestFileSelectorChain:
    @pytest.fixture
    def notes_md(self, tmp_path):
        path = f"{tmp_path}/notes.md"
        with open(path, "w") as f:
            f.write("This is a sample note.")
        return path

    @pytest.fixture
    def fitness_md(self, tmp_path):
        path = f"{tmp_path}/fitness.md"
        with open(path, "w") as f:
            f.write("This is my fitness journal!")
        return path

    @pytest.fixture
    def sleep_log_csv(self, tmp_path):
        path = f"{tmp_path}/sleep_log.csv"
        with open(path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(
                [
                    ["fell_asleep", "awoke", "duration"],
                    ["2024-01-01 23:00", "2022-01-02 07:00", "08:00"],
                    ["2024-01-02 23:30", "2022-01-03 08:00", "08:30"],
                ]
            )
        return path

    def test_file_selector_chain_selects_existing_file(
        self, notes_md, fitness_md, sleep_log_csv
    ):
        model = ChatOpenAI(model="gpt-4o-mini")
        chain = FileSelectorChain(model=model)
        with patch_model_responses([fitness_md]):
            result = chain.invoke(
                {
                    "content": "Went on a run yesterday!",
                    "files": [notes_md, fitness_md, sleep_log_csv],
                }
            )

        assert result.get("existing_file_path") == fitness_md
        assert result.get("new_file_path") is None

    def test_file_selector_chain_selects_new_file(
        self, notes_md, fitness_md, sleep_log_csv
    ):
        model = ChatOpenAI(model="gpt-4o-mini")
        chain = FileSelectorChain(model=model)

        new_file_name = "diet_log.csv"
        with patch_model_responses([new_file_name]):
            result = chain.invoke(
                {
                    "content": "Had oatmeal for breakfast and then a salad for lunch.",
                    "files": [notes_md, fitness_md, sleep_log_csv],
                }
            )

        assert result.get("existing_file_path") is None
        assert result.get("new_file_path") == new_file_name
