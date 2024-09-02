from unittest.mock import MagicMock, patch

from langchain_core.messages import BaseMessage


def patch_model_responses(responses):
    return patch(
        "langchain_openai.ChatOpenAI.invoke",
        side_effect=[
            MagicMock(spec=BaseMessage, content=response, text=str(response))
            for response in responses
        ],
    )


def patch_json_parsing(result):
    return patch(
        "langchain_core.output_parsers.json.JsonOutputParser.parse_result",
        side_effect=[result],
    )
