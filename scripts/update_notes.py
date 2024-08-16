import time

from watchdog.observers import Observer

from capture import settings
from capture.event_handlers import TextFileHandler
from capture.notes.notes_service import NotesService


def add_content(file):
    with open(file, "r") as f:
        content = f.read()

    notes = NotesService(settings.NOTES_DIRECTORY, settings.FOOD_LOG_PATH)
    notes.add_content(content)


if __name__ == "__main__":
    event_handler = TextFileHandler(add_content)
    observer = Observer()
    observer.schedule(event_handler, path=settings.FILE_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
