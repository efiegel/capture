import whisper


class Audio:
    def __init__(self, model_size: str = "medium"):
        self.model_size = model_size
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_file_path: str, transcription_file_path: str) -> str:
        model_transcription = self.model.transcribe(audio_file_path)
        with open(transcription_file_path, "w") as f:
            f.write(model_transcription["text"])

        return model_transcription
