from typing import Optional

from langchain.chains.base import Chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import create_model


class SchemaInferenceChain(Chain):
    model: ChatOpenAI

    @property
    def chain(self):
        system_message = """
        You are an expert in data analysis and schema inference. You will be provided
        data that needs to be understood and converted into a schema for a CSV file. The
        data may be the first few rows of a CSV file itself or a block of text that will
        be parsed later and then written to a CSV. If you are given a block of text, 
        pull out the relevant pieces of data that would be written to the CSV and ignore 
        extraneous language describing the event or file itself. Your ultimate task is 
        to infer the schema of the final CSV file and return it in exactly this format: 
        'field_name: field_type, field_name: field_type, ...'. All names should be snake
        case. Types should be one of 'str', 'int', 'float', 'bool'. Return only the 
        schema, nothing else.
        """

        template = """
        {system_message}
        Data:
        {data}
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["data"],
            partial_variables={"system_message": system_message},
        )

        return prompt | self.model

    @property
    def input_keys(self) -> list[str]:
        return ["data"]

    @property
    def output_keys(self) -> list[str]:
        return ["schema"]

    def _call(self, inputs):
        response = self.chain.invoke(inputs)
        schema_dict = self._parse_schema_string(response.content)
        return {"schema": create_model("InferredSchema", **schema_dict)}

    @staticmethod
    def _parse_schema_string(schema_string: str) -> dict:
        type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }

        schema_dict = {}
        for field in schema_string.replace(" ", "").split(","):
            name, type_str = field.split(":")
            field_type = Optional[type_mapping.get(type_str)]
            schema_dict[name] = (field_type, ...)

        return schema_dict
