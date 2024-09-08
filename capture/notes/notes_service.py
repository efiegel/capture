import os
from datetime import datetime

from capture.llm import Agent
from capture.notes.CSVNote import CSVNote


class NotesService:
    def __init__(self, notes_directory: str) -> None:
        self.notes_directory = notes_directory
        self.agent = Agent("gpt-4o-mini")

    def get_or_create_daily_note(self) -> str:
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        file_path = os.path.join(self.notes_directory, "daily_notes", file_name)
        if not os.path.exists(file_path):
            self.write("", file_path)
        return file_path

    def update_note(self, file_path, new_content):
        with open(file_path, "r") as f:
            existing_content = f.read()

        updated_content = self.agent.integrate(existing_content, new_content)
        self.write(updated_content, file_path)

    def write(self, content: str, note_path: str):
        with open(note_path, "w") as f:
            f.write(content)

    def add_content_to_daily_note(self, content: str):
        daily_note = self.get_or_create_daily_note()
        self.update_note(daily_note, content)

    def add_content_to_csv_note(self, file_path: str, content: str):
        note = CSVNote(file_path)
        csv_data = note.get_first_n_lines(5)
        schema = self.agent.infer_csv_schema(csv_data)
        entries = self.agent.parse(content, list[schema])
        note.add_entries(entries)

    def _list_files_in_directory(self, directory: str):
        files = []
        for root, dirs, filenames in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in filenames:
                if not filename.startswith("."):
                    files.append(os.path.join(root, filename))
        return files

    def _drop_common_file_root(self, files: list[str], root: str):
        root = os.path.expanduser(root)
        return [os.path.relpath(file, root) for file in files]

    def _get_note_files(self):
        files = self._list_files_in_directory(self.notes_directory)
        return self._drop_common_file_root(files, self.notes_directory)

    def add_content(self, content: str):
        file = self.agent.select_file(content, self._get_note_files())
        if file.endswith(".csv"):
            self.add_content_to_csv_note(file, content)
        else:
            self.add_content_to_daily_note(content)
