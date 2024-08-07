import os
import shutil
import time

from watchdog.observers import Observer

from capture.event_handlers import M4AFileHandler

SOURCE_AUDIO_DIRECTORY = os.path.expanduser(
    "~/Library/Application Support/com.apple.voicememos/Recordings"
)
RAW_AUDIO_DIRECTORY = "data/audio/raw"


def copy(file):
    file_name = os.path.basename(file)
    source_path = os.path.join(SOURCE_AUDIO_DIRECTORY, file_name)
    dest_path = os.path.join(RAW_AUDIO_DIRECTORY, file_name)
    shutil.copy(source_path, dest_path)


if __name__ == "__main__":
    event_handler = M4AFileHandler(copy)
    observer = Observer()
    observer.schedule(event_handler, path=SOURCE_AUDIO_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
