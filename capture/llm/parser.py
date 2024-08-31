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
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.vectorstore = Chroma(
            persist_directory=VECTORSTORE_PATH,
            embedding_function=OpenAIEmbeddings(),
        )

    @property
    def chain(self):
        system_message = f"""
        You are an expert at parsinglog entries. You will be provided with a text
        snippet and you will need to parse out the relevant information. When parsing 
        if time information is needed, just use best judgement on the time of day and
        know that it should be for today, {datetime.now()}. You may also be provided 
        additional relevant context to aid your parsing task.
        """

        parser = PydanticOutputParser(pydantic_object=self._get_chain_response_model())

        prompt = PromptTemplate(
            template="{system_message}\n{format_instructions}\n{context}\n{content}\n",
            input_variables=["content"],
            partial_variables={
                "system_message": system_message,
                "format_instructions": parser.get_format_instructions(),
                "context": self.vectorstore.as_retriever() | format_docs,
            },
        )

        return prompt | self.model | parser

    def parse(self, content: str):
        model_response = self.chain.invoke({"content": content})
        if self._response_format_is_list():
            return model_response.items
        return model_response

    def _response_format_is_list(self) -> bool:
        return self.response_format.__origin__ is list

    def _get_chain_response_model(self) -> BaseModel:
        if self._response_format_is_list():
            item_type = self.response_format.__args__[0]
            return create_model("Items", items=(List[item_type], ...))
        return self.response_format
