from time import time

import whisper

from capture.db import AudioTranscription, RawAudio


class Audio:
    def __init__(self, model_size: str = "medium"):
        self.model_size = model_size
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_file_path: str, transcription_file_path: str) -> str:
        raw_audio = RawAudio.create(file_path=audio_file_path)
        raw_audio.save()

        start = time()
        model_transcription = self.model.transcribe(audio_file_path)
        end = time()

        transcription_text = model_transcription["text"]
        with open(transcription_file_path, "w") as f:
            f.write(transcription_text)

        transcription = AudioTranscription.create(
            file_path=transcription_file_path,
            raw_audio=raw_audio,
            model=f"whisper-{self.model_size}",
            transcription_time_seconds=end - start,
        )
        transcription.save()

        return model_transcription
