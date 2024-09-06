from langchain.chains.base import Chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class IntegratorChain(Chain):
    model: ChatOpenAI

    @property
    def chain(self):
        system_message = """
        You are an expert at writing markdown and note-taking. You will be provided with
        existing content of a markdown file and also new content that needs to be
        added to the file. Please integrate the new content into the existing 
        content in a coherent and organized manner. Return only the updated content of 
        the markdown file, and do so without the ``` characters before and after.
        """

        template = """
        {system_message}
        Existing content: '{existing_content}'
        New content: '{new_content}'
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["existing_content", "new_content"],
            partial_variables={"system_message": system_message},
        )

        return prompt | self.model

    @property
    def input_keys(self) -> list[str]:
        return ["existing_content", "new_content"]

    @property
    def output_keys(self) -> list[str]:
        return ["updated_content"]

    def _call(self, inputs):
        response = self.chain.invoke(inputs)
        return {"updated_content": response.content}
