from unittest.mock import MagicMock, patch

from capture.sources.apple_notes import AppleNotesSource


class TestAppleNotesSource:
    def test_get_notes(self):
        mock_app = MagicMock()
        folder = MagicMock()
        with patch("capture.sources.apple_notes.SBApplication", return_value=mock_app):
            apple_notes_source = AppleNotesSource("capture")
            with patch.object(apple_notes_source, "_get_folder", return_value=folder):
                notes = apple_notes_source.get_notes()
                assert notes == []
