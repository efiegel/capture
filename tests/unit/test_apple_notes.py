from markdownify import markdownify as md
from ScriptingBridge import SBApplication


def test_apple_notes():
    apple_notes_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Notes")
    folder_name = "capture"
    account_name = "iCloud"

    notes = []
    # can also fetch the default account at apple_notes_app.accounts()[0]
    for account in apple_notes_app.accounts():
        if account.name() == account_name:
            folders = account.folders()
            for folder in folders:
                if folder.name() == folder_name:
                    notes = folder.notes()
                    break
            break

    if notes:
        latest_note = notes[0]
        print("id:", latest_note.id())
        print("name:", latest_note.name())
        print("body:", latest_note.body())
        print("body as markdown:", md(latest_note.body()))
        print("creation date:", latest_note.creationDate())
        print("modification date:", latest_note.modificationDate())
