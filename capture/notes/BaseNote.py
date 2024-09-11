from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseNote(ABC, Generic[T]):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._contents = None

    @property
    def contents(self) -> T:
        if self._contents is None:
            self._contents = self.read()
        return self._contents

    @contents.setter
    def contents(self, new_content: T):
        self._contents = new_content

    @abstractmethod
    def read(self) -> T:
        pass

    @abstractmethod
    def write(self, content: T):
        pass
