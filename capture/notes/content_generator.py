from datetime import datetime

from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from capture.notes.food_log import FoodLogEntry


class ContentGenerator:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini")

    def choose_category(self, content: str, categories: list[str]) -> str:
        system_message = """
        You are an expert at categorizing content. You will be provided with a sample
        of text and a list of categories. Your task is to choose the category that best
        fits the text. Return only the name of the category.
        """

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Sample: '{content}'. : '{categories}'."),
        ]

        response = self.model.invoke(messages)

        return response.content

    def parse_food_log_entries(self, content: str) -> list[FoodLogEntry]:
        system_message = f"""
        You are an expert at parsing food log entries. You will be provided with a text
        snippet and you will need to parse out the relevant information. When parsing 
        the datetime a food was eaten, just use best judgement on the time of day and
        know that it should be for today, {datetime.now()}.
        """

        class ResponseFormat(BaseModel):
            entries: list[FoodLogEntry]

        parser = PydanticOutputParser(pydantic_object=ResponseFormat)

        prompt = PromptTemplate(
            template="{system_message}\n{format_instructions}\n{content}\n",
            input_variables=["content"],
            partial_variables={
                "system_message": system_message,
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | self.model | parser
        response = chain.invoke({"content": content})

        return response.entries

    def integrate_content(self, existing_content: str, new_content: str) -> str:
        system_message = """
        You are an expert at writing markdown and note-taking. You will be provided with
        existing content of a markdown file and also new information that needs to be
        added to the file. Please integrate the new information into the existing 
        content in a coherent and organized manner. Return only the updated content of 
        the markdown file, and do so without the ``` characters before and after.
        """

        user_message = f"""
        Existing content: '{existing_content}'. New information: '{new_content}'.
        """

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message),
        ]

        response = self.model.invoke(messages)

        return response.content
