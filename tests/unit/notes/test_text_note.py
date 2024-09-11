from capture.notes import TextNote


class TestTextNote:
    def test_write_to_note(self, tmp_path):
        note = TextNote(f"{tmp_path}/note.md")
        content = "Hello, World!"
        note.write(content)

        with open(note.file_path) as file:
            assert file.read() == content
