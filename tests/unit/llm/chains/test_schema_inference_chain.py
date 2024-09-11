from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from capture.llm.chains import SchemaInferenceChain
from tests.utils import patch_model_responses


class TestSchemaInferenceChain:
    def test_schema_inference_chain(self):
        data = """
            First Name,age,city
            Alice,30,New York
            Bob,25,Los Angeles
            Charlie,35,Chicago
            """

        model = ChatOpenAI(model="gpt-4o-mini")
        chain = SchemaInferenceChain(model=model)
        with patch_model_responses(["first_name: str, age: int, city: str"]):
            inferred_schema = chain.invoke({"data": data})["schema"]

        class InferredSchema(BaseModel):
            first_name: str
            age: int
            city: str

        assert issubclass(inferred_schema, BaseModel)
        assert inferred_schema.model_json_schema() == InferredSchema.model_json_schema()
