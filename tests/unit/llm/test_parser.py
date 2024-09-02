from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from capture.llm import Parser


def patch_json_parsing(result):
    return patch(
        "langchain_core.output_parsers.json.JsonOutputParser.parse_result",
        side_effect=[result],
    )


class TestParser:
    @pytest.fixture()
    def model(self):
        class Model(BaseModel):
            attr1: str
            attr2: int

        return Model

    def test_parse_per_model(self, model):
        parser = Parser(model)
        parsed_result_dict = {"attr1": "1", "attr2": 2}
        with patch_json_parsing(parsed_result_dict):
            assert parser.parse(MagicMock()) == model(**parsed_result_dict)

    def test_parse_for_list(self, model):
        parser = Parser(list[model])
        parsed_result_dict = {"attr1": "1", "attr2": 2}
        with patch_json_parsing({"items": [parsed_result_dict]}):
            parser.parse(MagicMock()) == [model(**parsed_result_dict)]
