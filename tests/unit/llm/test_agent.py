from unittest.mock import MagicMock

import pytest
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel

from capture.llm import Agent
from tests.utils import patch_json_parsing, patch_model_responses


class TestAgent:
    @pytest.fixture()
    def response_model(self):
        class Model(BaseModel):
            attr1: str
            attr2: int

        return Model

    @pytest.fixture()
    def vectorstore(self):
        return Chroma(embedding_function=OpenAIEmbeddings())

    @pytest.fixture()
    def agent(self, vectorstore):
        return Agent(model_name="gpt-4o-mini", vectorstore=vectorstore)

    def test_parse_per_model(self, agent, response_model):
        parsed_result_dict = {"attr1": "1", "attr2": 2}
        with patch_model_responses([None]):
            with patch_json_parsing(parsed_result_dict):
                content = MagicMock()
                response_format = response_model
                expected_output = response_model(**parsed_result_dict)
                assert agent.parse(content, response_format) == expected_output

    def test_parse_for_list(self, agent, response_model):
        parsed_result_dict = {"attr1": "1", "attr2": 2}
        with patch_model_responses([None]):
            with patch_json_parsing({"items": [parsed_result_dict]}):
                content = MagicMock()
                response_format = list[response_model]
                expected_output = [response_model(**parsed_result_dict)]
                assert agent.parse(content, response_format) == expected_output
