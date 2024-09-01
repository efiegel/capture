from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class Integrator:
    def __init__(self, existing_markdown_content: str) -> None:
        self.existing_markdown_content = existing_markdown_content

    def integrate_markdown(self, new_content: str) -> str:
        system_message = """
        You are an expert at writing markdown and note-taking. You will be provided with
        existing content of a markdown file and also new information that needs to be
        added to the file. Please integrate the new information into the existing 
        content in a coherent and organized manner. Return only the updated content of 
        the markdown file, and do so without the ``` characters before and after.
        """

        user_message = f"""
        Existing content: '{self.existing_markdown_content}'.
        New information: '{new_content}'.
        """

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message),
        ]

        model = ChatOpenAI(model="gpt-4o-mini")
        response = model.invoke(messages)

        return response.content
