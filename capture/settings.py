import os

from dotenv import load_dotenv

load_dotenv()

# Audio directories
SOURCE_AUDIO_DIRECTORY = (
    os.path.expanduser(os.getenv("SOURCE_AUDIO_DIRECTORY", "")) or None
)
RAW_AUDIO_DIRECTORY = os.getenv("RAW_AUDIO_DIRECTORY")
TRANSCRIPTION_DIRECTORY = os.getenv("TRANSCRIPTION_DIRECTORY")

# Note directories
FILE_DIRECTORY = os.getenv("TRANSCRIPTION_DIRECTORY")
NOTES_DIRECTORY = os.path.expanduser(os.getenv("NOTES_DIRECTORY", "")) or None

# Vectorstore
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH")

# Secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
