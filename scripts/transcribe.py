import os
import time

from watchdog.observers import Observer

from capture import settings
from capture.audio import Audio
from scripts.event_handlers import M4AFileHandler


def transcribe(file):
    file_name = os.path.basename(file)
    transcriber = Audio("tiny")
    transcriber.transcribe(file, f"{settings.TRANSCRIPTION_DIRECTORY}/{file_name}.txt")


if __name__ == "__main__":
    event_handler = M4AFileHandler(transcribe, 0)
    observer = Observer()
    observer.schedule(event_handler, path=settings.RAW_AUDIO_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
