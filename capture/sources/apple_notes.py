from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ScriptingBridge import SBApplication


@dataclass
class AppleNote:
    id: str
    title: str
    content: str
    creation_date: str
    modification_date: str


class AppleNotes:
    def __init__(
        self,
        apple_notes_app: SBApplication,
        folder_name: str,
        account_name: str = "iCloud",
    ) -> None:
        self.apple_notes_app = apple_notes_app
        self.folder_name = folder_name
        self.account_name = account_name

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
