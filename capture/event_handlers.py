import os
import subprocess
import time

from watchdog.events import FileSystemEventHandler


class M4AFileHandler(FileSystemEventHandler):
    def __init__(self, on_created_callback) -> None:
        super().__init__()
        self.on_created_callback = on_created_callback

    def on_created(self, event):
        file = event.src_path
        if file.endswith(".m4a"):
            if self.is_file_ready(file):
                self.on_created_callback(file)

    def is_file_ready(self, file_path, wait_time=2, max_attempts=20):
        previous_size = -1
        for _ in range(max_attempts):
            current_size = os.path.getsize(file_path)
            if current_size == previous_size and self.is_valid_audio(file_path):
                return True
            previous_size = current_size
            time.sleep(wait_time)
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
