from dataclasses import dataclass
from typing import Iterator

from ScriptingBridge import SBApplication


@dataclass
class AppleNote:
    id: str
    content: str
    creation_date: str
    modification_date: str


class AppleNotes:
    def __init__(self, folder_name: str, account_name: str = "iCloud") -> None:
        self.folder_name = folder_name
        self.account_name = account_name
        self.apple_notes_app = SBApplication.applicationWithBundleIdentifier_(
            "com.apple.Notes"
        )

    def note_iterator(self) -> Iterator[AppleNote]:
        if (folder := self._get_folder()) is None:
            return iter([])

        if (notes := folder.notes()) is None:
            return iter([])

        for note in notes:
            yield self._convert_to_dataclass(note)

    def _convert_to_dataclass(self, note) -> AppleNote:
        return AppleNote(
            id=note.id(),
            content=note.body(),
            creation_date=note.creationDate(),
            modification_date=note.modificationDate(),
        )

    def _get_folder(self):
        for account in self.apple_notes_app.accounts():
            if account.name() == self.account_name:
                folders = account.folders()
                for folder in folders:
                    if folder.name() == self.folder_name:
                        return folder
        return None
