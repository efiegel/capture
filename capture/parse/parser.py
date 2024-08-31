from pydantic import BaseModel


class Parser:
    def __init__(self, schema: BaseModel) -> None:
        pass

    def parse(self, content: str) -> str:
        pass
