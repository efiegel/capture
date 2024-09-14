import os
from typing import List, Type, Union

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, create_model

from .chains import (
    FileSelectorChain,
    IntegratorChain,
    ParserChain,
    SchemaInferenceChain,
)


class Agent:
    def __init__(self, model_name: str, vectorstore: Chroma):
        self.model = ChatOpenAI(model=model_name)
        self.vectorstore = vectorstore

    def integrate(self, existing_content: str, new_content: str):
        chain = IntegratorChain(model=self.model)
        inputs = {"existing_content": existing_content, "new_content": new_content}
        response = chain.invoke(inputs)
        return response.get("updated_content")

    def infer_schema(self, data: str) -> Type[BaseModel]:
        chain = SchemaInferenceChain(model=self.model)
        response = chain.invoke({"data": data})
        return response.get("schema")

    def select_file(self, directory: str, content: str) -> str:
        files_full_paths = self._list_files_in_directory(directory)
        files = self._drop_common_path_root(files_full_paths, directory)

        chain = FileSelectorChain(model=self.model)
        response = chain.invoke({"content": content, "files": files})
        file = response.get("existing_file_path") or response.get("new_file_path")
        return os.path.join(directory, file)

    def parse(
        self,
        content: str,
        response_format: Union[Type[BaseModel], Type[list[BaseModel]]],
    ):
        if response_format.__class__ == BaseModel.__class__:
            chain = ParserChain(
                model=self.model,
                response_format=response_format,
                vectorstore=self.vectorstore,
            )
            return chain.invoke({"content": content}).get("parsed_content")
        else:
            items_model = self._create_items_model(response_format)
            chain = ParserChain(
                model=self.model,
                response_format=items_model,
                vectorstore=self.vectorstore,
            )
            return chain.invoke({"content": content}).get("parsed_content").items

    @staticmethod
    def _create_items_model(obj: Type[list[BaseModel]]):
        return create_model("Items", items=(List[obj.__args__[0]], ...))

    @staticmethod
    def _list_files_in_directory(directory: str):
        files = []
        for root, dirs, filenames in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in filenames:
                if not filename.startswith("."):
                    files.append(os.path.join(root, filename))
        return files

    @staticmethod
    def _drop_common_path_root(files: list[str], root: str):
        root = os.path.expanduser(root)
        return [os.path.relpath(file, root) for file in files]
