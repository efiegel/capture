from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class IntegratorChain:
    def __init__(self, model: ChatOpenAI):
        self.model = model

    @property
    def chain(self):
        system_message = """
        You are an expert at writing markdown and note-taking. You will be provided with
        existing content of a markdown file and also new information that needs to be
        added to the file. Please integrate the new information into the existing 
        content in a coherent and organized manner. Return only the updated content of 
        the markdown file, and do so without the ``` characters before and after.
        """

        template = """
        {system_message}
        Existing content: '{existing_content}'
        New information: '{new_information}'
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["content", "categories"],
            partial_variables={"system_message": system_message},
        )

        return prompt | ChatOpenAI(model="gpt-4o-mini")

    def invoke(self, *args, **kwargs):
        return self.chain.invoke(*args, **kwargs)
