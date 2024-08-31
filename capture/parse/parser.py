from pydantic import BaseModel

from capture.llm.chains import ParserChain


class Parser:
    def __init__(self, schema: BaseModel) -> None:
        self.chain = ParserChain(schema)

    def parse(self, content: str) -> str:
        response = self.chain.invoke({"content": content})
        return response.entries
