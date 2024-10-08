import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

from capture.llm import Agent
from capture.notes import BaseNote, CSVNote, TextNote


class Vault:
    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.dot_dir = self._get_or_init_dot_dir()
        self.agent = Agent(
            "gpt-4o-mini",
            vectorstore=Chroma(
                persist_directory=os.path.join(self.dot_dir, ".chroma"),
                embedding_function=OpenAIEmbeddings(),
            ),
        )

    def _get_or_init_dot_dir(self):
        dir = os.path.join(self.directory, ".capture")
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def add(self, content: str):
        file = self.agent.select_file(self.directory, content)
        note = self._get_or_init_note(file)
        if isinstance(note, CSVNote):
            self._add_to_csv_note(note, content)
        else:
            self._add_to_text_note(note, content)

    def _add_to_text_note(self, note: TextNote, content: str):
        existing_content = note.read()
        updated_content = self.agent.integrate(existing_content, content)
        note.write(updated_content)

    def _add_to_csv_note(self, note: CSVNote, content: str):
        first_lines = note.read()[:5]
        schema = self.agent.infer_schema(first_lines or content)
        entries = self.agent.parse(content, list[schema])
        if not first_lines:
            note.write([list(schema.model_fields.keys())])
        note.write([list(entry.model_dump().values()) for entry in entries])

    def _get_or_init_note(self, file_path: str) -> BaseNote:
        if not os.path.exists(file_path):
            Path(file_path).touch()
        if file_path.endswith(".csv"):
            return CSVNote(file_path)
        else:
            return TextNote(file_path)
