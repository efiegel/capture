from capture.audio import Audio
from capture.db import database_context

RAW_AUDIO_DIRECTORY = "data/audio/raw"
TRANSCRIPTION_DIRECTORY = "data/audio/transcriptions"

with database_context():
    file = "sample1.m4a"
    transcriber = Audio("tiny")
    transcriber.transcribe(
        f"{RAW_AUDIO_DIRECTORY}/{file}", f"{TRANSCRIPTION_DIRECTORY}/{file}.txt"
    )
