from unittest.mock import patch

from langchain_openai import OpenAIEmbeddings

from capture.rag import load_csv_data
from capture.settings import VECTORSTORE_PATH


class TestRAG:
    def test_load_csv_data_calls_chroma_correctly(self):
        docs = []
        loader = "langchain_community.document_loaders.csv_loader.CSVLoader.load"
        with patch(loader, return_value=docs):
            with patch("langchain_chroma.Chroma.from_documents") as chroma_mock:
                load_csv_data("")

        chroma_mock.assert_called_once_with(
            documents=docs,
            embedding=OpenAIEmbeddings(),
            persist_directory=VECTORSTORE_PATH,
        )
