from datetime import datetime
from typing import List, Type, Union

from langchain.output_parsers import PydanticOutputParser
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, create_model

from capture.rag import format_docs
from capture.settings import VECTORSTORE_PATH


class Parser:
    def __init__(self, response_format: Union[Type[BaseModel], Type[list[BaseModel]]]):
        self.response_format = response_format

    def create_chain(self, parser_pydantic_object: Type[BaseModel]):
        system_message = f"""
        You are an expert at parsinglog entries. You will be provided with a text
        snippet and you will need to parse out the relevant information. When parsing 
        if time information is needed, just use best judgement on the time of day and
        know that it should be for today, {datetime.now()}. You may also be provided 
        additional relevant context to aid your parsing task.
        """

        vectorstore = Chroma(
            persist_directory=VECTORSTORE_PATH, embedding_function=OpenAIEmbeddings()
        )

        parser = PydanticOutputParser(pydantic_object=parser_pydantic_object)
        model = ChatOpenAI(model="gpt-4o-mini")
        prompt = PromptTemplate(
            template="{system_message}\n{format_instructions}\n{context}\n{content}\n",
            input_variables=["content"],
            partial_variables={
                "system_message": system_message,
                "format_instructions": parser.get_format_instructions(),
                "context": vectorstore.as_retriever() | format_docs,
            },
        )

        return prompt | model | parser

    def parse(self, content: str):
        if self.response_format.__origin__ is list:
            chain = self.create_chain(self._create_items_model(self.response_format))
            return chain.invoke({"content": content}).items
        else:
            chain = self.create_chain(self.response_format)
            return chain.invoke({"content": content})

    @staticmethod
    def _create_items_model(obj: Type[list[BaseModel]]):
        return create_model("Items", items=(List[obj.__args__[0]], ...))
