import os
import subprocess

from dotenv import load_dotenv
from ScriptingBridge import SBApplication

from capture.sources.apple_notes import AppleNotes
from capture.vault import Vault

load_dotenv()

VAULT_DIRECTORY = os.path.expanduser(os.getenv("VAULT_DIRECTORY", ""))


def close_notes_app():
    script = 'tell application "Notes" to quit'
    subprocess.run(["osascript", "-e", script])


def notes_is_open():
    script = 'tell application "System Events" to (name of processes) contains "Notes"'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip() == "true"


if __name__ == "__main__":
    close_notes_when_done = True if not notes_is_open() else False

    vault = Vault(VAULT_DIRECTORY)
    apple_notes_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Notes")
    apple_notes_source = AppleNotes(apple_notes_app, "capture")
    for note in apple_notes_source.note_iterator():
        print("-" * 40)
        print(f"title: {note.title}")
        print(f"created at: {note.creation_date}")
        print(f"modified at: {note.modification_date}")

        user_input = input("  >> add to vault? (y/n) [y]: ").strip().lower() or "y"
        if user_input == "n":
            break

        vault.add(note)

    if close_notes_when_done:
        close_notes_app()
