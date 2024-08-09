import os
import shutil
import time

from dotenv import load_dotenv
from watchdog.observers import Observer

from capture.event_handlers import M4AFileHandler

load_dotenv()

SOURCE_AUDIO_DIRECTORY = os.path.expanduser(os.getenv("SOURCE_AUDIO_DIRECTORY"))
RAW_AUDIO_DIRECTORY = os.getenv("RAW_AUDIO_DIRECTORY")


def copy(file):
    file_name = os.path.basename(file)
    source_path = os.path.join(SOURCE_AUDIO_DIRECTORY, file_name)
    dest_path = os.path.join(RAW_AUDIO_DIRECTORY, file_name)
    shutil.copy(source_path, dest_path)


if __name__ == "__main__":
    max_recording_duration_seconds = 60 * 5  # 5 minutes
    event_handler = M4AFileHandler(copy, max_recording_duration_seconds)
    observer = Observer()
    observer.schedule(event_handler, path=SOURCE_AUDIO_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
