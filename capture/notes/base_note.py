from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseNote(ABC, Generic[T]):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def read(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def write(self, content: T):
        raise NotImplementedError
