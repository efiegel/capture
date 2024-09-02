from unittest.mock import patch


def patch_json_parsing(result):
    return patch(
        "langchain_core.output_parsers.json.JsonOutputParser.parse_result",
        side_effect=[result],
    )
