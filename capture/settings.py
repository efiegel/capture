import os

from dotenv import load_dotenv

load_dotenv()

FILE_DIRECTORY = os.getenv("TRANSCRIPTION_DIRECTORY")
NOTES_DIRECTORY = os.path.expanduser(os.getenv("NOTES_DIRECTORY"))
FOOD_LOG_PATH = os.path.expanduser(os.getenv("FOOD_LOG_PATH"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAW_AUDIO_DIRECTORY = os.getenv("RAW_AUDIO_DIRECTORY")
TRANSCRIPTION_DIRECTORY = os.getenv("TRANSCRIPTION_DIRECTORY")
