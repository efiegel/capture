from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


def load_csv_data(file_path: str, vectorstore_path: str):
    loader = CSVLoader(file_path=file_path)
    docs = loader.load()
    Chroma.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
        persist_directory=vectorstore_path,
    )


def format_docs(docs: list[Document]):
    return "\n\n".join(doc.page_content for doc in docs)
