from pathlib import Path

import pytest

from capture.notes import TextNote


class TestTextNote:
    @pytest.fixture
    def note_path(self, tmp_path):
        path = f"{tmp_path}/note.md"
        Path(path).touch()
        return path

    def test_write_to_note(self, note_path):
        note = TextNote(note_path)
        content = "Hello, World!"
        note.write(content)

        assert note.contents == content
        with open(note_path) as file:
            assert file.read() == content
