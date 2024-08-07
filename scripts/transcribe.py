import os
import time

from watchdog.observers import Observer

from capture.audio import Audio
from capture.db import database_context
from capture.event_handlers import M4AFileHandler

RAW_AUDIO_DIRECTORY = "data/audio/raw"
TRANSCRIPTION_DIRECTORY = "data/audio/transcriptions"


def transcribe(file):
    with database_context():
        file_name = os.path.basename(file)
        transcriber = Audio("tiny")
        transcriber.transcribe(file, f"{TRANSCRIPTION_DIRECTORY}/{file_name}.txt")


if __name__ == "__main__":
    event_handler = M4AFileHandler(transcribe)
    observer = Observer()
    observer.schedule(event_handler, path=RAW_AUDIO_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
