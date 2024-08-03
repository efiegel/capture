import whisper


class Audio:
    def __init__(self, model_size: str = "medium"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, filepath: str) -> str:
        return self.model.transcribe(filepath)
