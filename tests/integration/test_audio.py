import pytest

from capture.audio import Audio


class TestAudio:
    @pytest.fixture
    def transcriber(self):
        return Audio("tiny")

    def test_transcribe(self, transcriber):
        audio_sample_filepath = "tests/sample_data/audio/audio_sample_1.wav"
        transcription_file_path = "tests/sample_data/audio/transcription_sample_1.txt"
        transcription = transcriber.transcribe(
            audio_sample_filepath, transcription_file_path
        )
        assert (
            transcription["text"]
            .lstrip()
            .startswith("The boy was there when the sun rose.")
        )
