from dataclasses import dataclass
from typing import Iterator

from ScriptingBridge import SBApplication


@dataclass
class AppleNote:
    id: str
    title: str
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
        for note in self._get_notes():
            yield self._convert_raw_note_to_dataclass(note)

    def _convert_raw_note_to_dataclass(self, note) -> AppleNote:
        return AppleNote(
            id=note.id(),
            title=note.name(),
            content=note.body(),
            creation_date=note.creationDate(),
            modification_date=note.modificationDate(),
        )

    def _get_notes(self):
        for account in self.apple_notes_app.accounts():
            if account.name() == self.account_name:
                folders = account.folders()
                for folder in folders:
                    if folder.name() == self.folder_name:
                        return folder.notes()
        return []
