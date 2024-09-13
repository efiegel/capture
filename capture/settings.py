import os

from dotenv import load_dotenv

load_dotenv()

VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
