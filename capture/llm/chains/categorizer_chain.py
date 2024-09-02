from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class CategorizerChain:
    @property
    def chain(self):
        system_message = """
        You are an expert at categorizing content. You will be provided with a sample
        of text and a list of categories. Your task is to choose the category that best
        fits the text. Return only the name of the category.
        """

        template = """
        {system_message}
        Sample: '{content}'
        Categories: '{categories}'
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["content", "categories"],
            partial_variables={"system_message": system_message},
        )

        return prompt | ChatOpenAI(model="gpt-4o-mini")
