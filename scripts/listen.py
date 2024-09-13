import time

import whisper
from watchdog.observers import Observer

from capture import settings
from capture.notes.notes_service import NotesService
from scripts.event_handlers import M4AFileHandler


def capture(file):
    model = whisper.load_model("small")
    transcription = model.transcribe(file)["text"]

    notes = NotesService(settings.NOTES_DIRECTORY)
    notes.add_content(transcription)


if __name__ == "__main__":
    max_recording_duration_seconds = 5 * 60
    event_handler = M4AFileHandler(capture, max_recording_duration_seconds)
    observer = Observer()
    observer.schedule(
        event_handler, path=settings.SOURCE_AUDIO_DIRECTORY, recursive=False
    )
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
