import os
import time

from dotenv import load_dotenv
from watchdog.observers import Observer

from capture.event_handlers import TextFileHandler
from capture.notes import Notes

load_dotenv()

FILE_DIRECTORY = os.getenv("TRANSCRIPTION_DIRECTORY")
NOTES_DIRECTORY = os.getenv("NOTES_DIRECTORY")
FOOD_LOG_PATH = os.getenv("FOOD_LOG_PATH")


def add_content(file):
    notes = Notes(
        os.path.expanduser(NOTES_DIRECTORY), os.path.expanduser(FOOD_LOG_PATH)
    )
    notes.add_content(file)


if __name__ == "__main__":
    event_handler = TextFileHandler(add_content)
    observer = Observer()
    observer.schedule(event_handler, path=FILE_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
