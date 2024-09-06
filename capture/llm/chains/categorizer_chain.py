from langchain.chains.base import Chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class CategorizerChain(Chain):
    model: ChatOpenAI

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

        return prompt | self.model

    @property
    def input_keys(self) -> list[str]:
        return ["content", "categories"]

    @property
    def output_keys(self) -> list[str]:
        return ["category"]

    def _call(self, inputs):
        response = self.chain.invoke(inputs)
        return {"category": response.content}
