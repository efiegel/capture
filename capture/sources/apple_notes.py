from dataclasses import dataclass

from ScriptingBridge import SBApplication


@dataclass
class SourceContent:
    id: str
    content: str
    creation_date: str
    modification_date: str


class AppleNotesSource:
    def __init__(self, folder_name: str, account_name: str = "iCloud") -> None:
        self.folder_name = folder_name
        self.account_name = account_name
        self.apple_notes_app = SBApplication.applicationWithBundleIdentifier_(
            "com.apple.Notes"
        )

    def get_notes(self):
        if (folder := self._get_folder()) is None:
            return []

        notes = folder.notes()
        return [
            SourceContent(
                id=note.id(),
                content=note.body(),
                creation_date=note.creationDate(),
                modification_date=note.modificationDate(),
            )
            for note in notes
        ]

    def _get_folder(self):
        for account in self.apple_notes_app.accounts():
            if account.name() == self.account_name:
                folders = account.folders()
                for folder in folders:
                    if folder.name() == self.folder_name:
                        return folder
        return None
