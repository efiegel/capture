from typing import List, Type, Union

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, create_model

from .chains import CategorizerChain, IntegratorChain, ParserChain


class Agent:
    def __init__(self, model_name: str):
        self.model = ChatOpenAI(model=model_name)

    def categorize(self, content: str, categories: list[str]) -> str:
        chain = CategorizerChain(model=self.model)
        inputs = {"content": content, "categories": categories}
        response = chain.invoke(inputs)
        return response.get("category")

    def integrate(self, existing_content: str, new_content: str):
        chain = IntegratorChain(model=self.model)
        inputs = {"existing_content": existing_content, "new_content": new_content}
        response = chain.invoke(inputs)
        return response.get("updated_content")

    def parse(
        self,
        content: str,
        response_format: Union[Type[BaseModel], Type[list[BaseModel]]],
    ):
        if response_format.__class__ == BaseModel.__class__:
            chain = ParserChain(model=self.model, response_format=response_format)
            return chain.invoke({"content": content}).get("content")
        else:
            items_model = self._create_items_model(response_format)
            chain = ParserChain(model=self.model, response_format=items_model)
            return chain.invoke({"content": content}).get("content").items

    @staticmethod
    def _create_items_model(obj: Type[list[BaseModel]]):
        return create_model("Items", items=(List[obj.__args__[0]], ...))
