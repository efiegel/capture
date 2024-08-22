from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings

from capture.settings import VECTORSTORE_PATH


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_csv_data(file_path):
    loader = CSVLoader(file_path=file_path)
    docs = loader.load()
    Chroma.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
        persist_directory=VECTORSTORE_PATH,
    )
