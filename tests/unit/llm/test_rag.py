from unittest.mock import MagicMock, patch

from capture.llm.rag import format_docs, load_csv_data


class TestRAG:
    def test_load_csv_data_calls_chroma_correctly(self):
        docs = []
        vectorstore_path = ""
        loader = "langchain_community.document_loaders.csv_loader.CSVLoader.load"
        embeddings = MagicMock()
        with patch(loader, return_value=docs):
            with patch("langchain_chroma.Chroma.from_documents") as chroma_mock:
                with patch("capture.llm.rag.OpenAIEmbeddings", return_value=embeddings):
                    load_csv_data("", vectorstore_path)

        chroma_mock.assert_called_once_with(
            documents=docs,
            embedding=embeddings,
            persist_directory=vectorstore_path,
        )

    def test_format_docs(self):
        docs = [MagicMock(page_content="doc 1"), MagicMock(page_content="doc 2")]
        formatted_docs = format_docs(docs)

        assert formatted_docs == "doc 1\n\ndoc 2"
