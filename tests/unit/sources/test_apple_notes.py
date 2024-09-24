from unittest.mock import MagicMock, patch

from capture.sources.apple_notes import AppleNote, AppleNotes


class TestAppleNotes:
    def test_note_iterator(self):
        "SBApplication is very arduous to mock. Necessary, but leads to an ugly test."

        app, account, folder, note = MagicMock(), MagicMock(), MagicMock(), MagicMock()
        mock_note = AppleNote(
            id="id",
            title="title",
            content="content",
            creation_date="2021-01-01",
            modification_date="2021-01-02",
        )

        with patch("capture.sources.apple_notes.SBApplication") as mock_sb_application:
            mock_sb_application.applicationWithBundleIdentifier_.return_value = app
            folder_name = "folder_name"
            a_notes = AppleNotes(folder_name)
            # fmt: off
            with patch.object(app, "accounts", return_value=[account]), \
                 patch.object(account, "name", return_value=a_notes.account_name), \
                 patch.object(account, "folders", return_value=[folder]), \
                 patch.object(folder, "name", return_value=folder_name), \
                 patch.object(folder, "notes", return_value=[note]), \
                 patch.object(note, "id", return_value="id"), \
                 patch.object(note, "name", return_value="title"), \
                 patch.object(note, "body", return_value="content"), \
                 patch.object(note,"creationDate",return_value="2021-01-01"), \
                 patch.object(note,"modificationDate", return_value="2021-01-02"):
                # fmt: on
                assert next(a_notes.note_iterator()) == mock_note
