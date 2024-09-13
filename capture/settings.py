import os

from dotenv import load_dotenv

load_dotenv()

AUDIO_DIRECTORY = os.path.expanduser(os.getenv("AUDIO_DIRECTORY", "")) or None
VAULT_DIRECTORY = os.path.expanduser(os.getenv("VAULT_DIRECTORY", "")) or None
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
