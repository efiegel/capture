import os
import time

from dotenv import load_dotenv
from watchdog.observers import Observer

from capture.event_handlers import TextFileHandler
from capture.notes import Notes

load_dotenv()

FILE_DIRECTORY = os.getenv("TRANSCRIPTION_DIRECTORY")
NOTES_DIRECTORY = os.getenv("NOTES_DIRECTORY")


def create_note(file):
    file_name = os.path.basename(file)
    note_path = os.path.expanduser(f"{NOTES_DIRECTORY}/{file_name}.md")

    notes = Notes()
    notes.insert(file, note_path)


if __name__ == "__main__":
    event_handler = TextFileHandler(create_note)
    observer = Observer()
    observer.schedule(event_handler, path=FILE_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
