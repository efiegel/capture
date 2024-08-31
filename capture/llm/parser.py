from datetime import datetime

from langchain.output_parsers import PydanticOutputParser
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel

from capture.rag import format_docs
from capture.settings import VECTORSTORE_PATH


class Parser:
    def __init__(self, response_format: BaseModel):
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

        parser = PydanticOutputParser(pydantic_object=self.response_format)

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
        return self.chain.invoke({"content": content})
