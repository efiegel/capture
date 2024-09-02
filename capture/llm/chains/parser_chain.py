from datetime import datetime

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from capture.llm.rag import format_docs, vectorstore


class ParserChain:
    def __init__(self, response_format: BaseModel):
        self.response_format = response_format

    @property
    def chain(self):
        system_message = f"""
        You are an expert at parsinglog entries. You will be provided with a text
        snippet and you will need to parse out the relevant information. When parsing 
        if time information is needed, just use best judgement on the time of day and
        know that it should be for today, {datetime.now()}. You may also be provided 
        additional relevant context to aid your parsing task.
        """

        template = """"
        {system_message}
        {format_instructions}
        {context}
        {content}
        """

        parser = PydanticOutputParser(pydantic_object=self.response_format)
        prompt = PromptTemplate(
            template=template,
            input_variables=["content"],
            partial_variables={
                "system_message": system_message,
                "format_instructions": parser.get_format_instructions(),
                "context": vectorstore.as_retriever() | format_docs,
            },
        )

        return prompt | ChatOpenAI(model="gpt-4o-mini") | parser
