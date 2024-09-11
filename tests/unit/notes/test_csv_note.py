import csv
from pathlib import Path

import pytest

from capture.notes import CSVNote


class TestCSVNote:
    @pytest.fixture
    def note_path(self, tmp_path):
        path = f"{tmp_path}/note.csv"
        Path(path).touch()
        return path

    def test_write_to_note_is_append_only_by_default(self, note_path):
        note = CSVNote(note_path)
        note.write([["a", "b", "c"]])
        note.write([["1", "2", "3"]])

        with open(note_path) as file:
            reader = csv.reader(file)
            assert list(reader) == [["a", "b", "c"], ["1", "2", "3"]]

    def test_write_to_note_can_overwrite(self, note_path):
        note = CSVNote(note_path)
        note.write([["a", "b", "c"]])
        note.write([["1", "2", "3"]], append=False)

        with open(note_path) as file:
            reader = csv.reader(file)
            assert list(reader) == [["1", "2", "3"]]
