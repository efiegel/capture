from datetime import datetime

from langchain.chains.base import Chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class FileSelectorChain(Chain):
    model: ChatOpenAI

    @property
    def chain(self):
        system_message = f"""
        You are an expert at selecting the correct file to which new information 
        should be added. You will be provided with text that needs to be added to a file
        and a list of files that it may belong to. Your task is to choose the file that
        best fits the text. However, it's entirely possible that no given file is best 
        and that a completely new file should be created. If that's the case, create a 
        new file name that maintains a consistent naming convention and path structure 
        with the other files that you have been supplied with. If you choose to create a
        new file, name it as if it already existed: don't name it 'new' or anything. For
        your reference, today is {datetime.now()}. Only return the chosen file path, and
        don't include any string-wrapping characters like `, ', or ".
        """

        template = """
        {system_message}
        New information: '{content}'
        Files: '{files}'
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["content", "files"],
            partial_variables={"system_message": system_message},
        )

        return prompt | self.model

    @property
    def input_keys(self) -> list[str]:
        return ["content", "files"]

    @property
    def output_keys(self) -> list[str]:
        return ["existing_file_path", "new_file_path"]

    def _call(self, inputs):
        existing_files = inputs["files"]
        response = self.chain.invoke(inputs)
        file = response.content
        if file not in existing_files:
            return {"new_file_path": file, "existing_file_path": None}
        return {"new_file_path": None, "existing_file_path": file}
