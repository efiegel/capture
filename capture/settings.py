import os

from dotenv import load_dotenv

load_dotenv()

# Audio directory
SOURCE_AUDIO_DIRECTORY = (
    os.path.expanduser(os.getenv("SOURCE_AUDIO_DIRECTORY", "")) or None
)

# Note directories
NOTES_DIRECTORY = os.path.expanduser(os.getenv("NOTES_DIRECTORY", "")) or None

# Vectorstore
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH")

# Secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
