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
        with the first few rows of a CSV file. Your task is to infer the schema of the 
        CSV and return it in exactly this format: 'field_name: field_type, field_name: 
        field_type, ...'. All names should be snake case. Types should be one of 'str',
        'int', 'float', 'bool'. Return only the schema, nothing else.
        """

        template = """
        {system_message}
        CSV data:
        {csv_data}
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["csv_data"],
            partial_variables={"system_message": system_message},
        )

        return prompt | self.model

    @property
    def input_keys(self) -> list[str]:
        return ["csv_data"]

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
            field_type = type_mapping.get(type_str)
            schema_dict[name] = (field_type, ...)

        return schema_dict
