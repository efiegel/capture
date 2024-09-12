import os

from capture.notes import TextNote


class TestTextNote:
    def test_write_to_note(self, tmp_path):
        note = TextNote(f"{tmp_path}/note.md")
        content = "Hello, World!"
        note.write(content)

        with open(note.file_path) as file:
            assert file.read() == content

    def test_read_note_that_does_not_exist_yet(self, tmp_path):
        note = TextNote(f"{tmp_path}/note.md")
        assert note.read() == ""
        assert not os.path.exists(note.file_path)
