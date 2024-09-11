import csv

from capture.notes import CSVNote


class TestCSVNote:
    def test_write_to_note_is_append_only_by_default(self, tmp_path):
        note = CSVNote(f"{tmp_path}/note.csv")
        note.write([["a", "b", "c"]])
        note.write([["1", "2", "3"]])

        with open(note.file_path) as file:
            reader = csv.reader(file)
            assert list(reader) == [["a", "b", "c"], ["1", "2", "3"]]

    def test_write_to_note_can_overwrite(self, tmp_path):
        note = CSVNote(f"{tmp_path}/note.csv")
        note.write([["a", "b", "c"]])
        note.write([["1", "2", "3"]], append=False)

        with open(note.file_path) as file:
            reader = csv.reader(file)
            assert list(reader) == [["1", "2", "3"]]
