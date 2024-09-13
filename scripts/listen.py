import os
import subprocess
import time

import whisper
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from capture import settings
from capture.vault import Vault


class M4AFileHandler(FileSystemEventHandler):
    def __init__(self, on_created_callback, total_wait_seconds) -> None:
        super().__init__()
        self.on_created_callback = on_created_callback
        self.total_wait_seconds = total_wait_seconds

    def on_created(self, event):
        file = event.src_path
        if file.endswith(".m4a"):
            if self.is_file_ready(file, self.total_wait_seconds):
                self.on_created_callback(file)

    def is_file_ready(self, file_path, total_wait_seconds):
        wait_interval_seconds = 2
        max_attempts = max(total_wait_seconds // wait_interval_seconds, 1)

        # quick accommodation for files that are already fully written (copies)
        if max_attempts == 1 and self.is_valid_audio(file_path):
            return True

        previous_size = -1
        for _ in range(max_attempts):
            current_size = os.path.getsize(file_path)
            if current_size == previous_size and self.is_valid_audio(file_path):
                return True
            previous_size = current_size
            time.sleep(wait_interval_seconds)
        return False

    def is_valid_audio(self, file_path):
        try:
            result = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", file_path, "-f", "null", "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result.returncode == 0
        except Exception:
            return False


def add_to_vault(file):
    model = whisper.load_model("small")
    transcription = model.transcribe(file)["text"]

    vault = Vault(settings.VAULT_DIRECTORY)
    vault.add(transcription)


if __name__ == "__main__":
    max_recording_duration_seconds = 5 * 60
    event_handler = M4AFileHandler(add_to_vault, max_recording_duration_seconds)
    observer = Observer()
    observer.schedule(event_handler, path=settings.AUDIO_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
