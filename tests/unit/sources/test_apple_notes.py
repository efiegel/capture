from unittest.mock import MagicMock, patch

from capture.sources.apple_notes import AppleNote, AppleNotes


class TestAppleNotes:
    def test_note_iterator(self):
        folder, notes = MagicMock(), [MagicMock()]
        mock_note = AppleNote(
            id="id",
            title="title",
            content="content",
            creation_date="2021-01-01",
            modification_date="2021-01-02",
        )

        with patch("capture.sources.apple_notes.SBApplication"):
            apple_notes = AppleNotes("capture")
            with patch.object(apple_notes, "_get_folder", return_value=folder):
                with patch.object(folder, "notes", return_value=notes):
                    with patch.object(
                        apple_notes, "_convert_to_dataclass", return_value=mock_note
                    ):
                        assert next(apple_notes.note_iterator()) == mock_note
