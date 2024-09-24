import os

from dotenv import load_dotenv
from ScriptingBridge import SBApplication

from capture.sources.apple_notes import AppleNotes
from capture.vault import Vault

load_dotenv()

VAULT_DIRECTORY = os.path.expanduser(os.getenv("VAULT_DIRECTORY", ""))


if __name__ == "__main__":
    vault = Vault(VAULT_DIRECTORY)
    apple_notes_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Notes")
    apple_notes_source = AppleNotes(apple_notes_app, "capture")
    for note in apple_notes_source.note_iterator():
        print("-" * 40)
        print(f"title: {note.title}")
        print(f"created at: {note.creation_date}")

        user_input = input("  >> add to vault? (y/n) [y]: ").strip().lower() or "y"
        if user_input == "n":
            break

        vault.add(note.content)
