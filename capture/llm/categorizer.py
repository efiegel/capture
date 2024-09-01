from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class Categorizer:
    def __init__(self, categories: list[str]) -> None:
        self.categories = categories

    def categorize(self, content: str) -> str:
        system_message = """
        You are an expert at categorizing content. You will be provided with a sample
        of text and a list of categories. Your task is to choose the category that best
        fits the text. Return only the name of the category.
        """
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Sample: '{content}'. : '{self.categories}'."),
        ]

        model = ChatOpenAI(model="gpt-4o-mini")
        response = model.invoke(messages)

        return response.content
