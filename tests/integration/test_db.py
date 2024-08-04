from capture.db import RawAudio


class TestDB:
    def test_raw_audio_model(self):
        file_path = "test_file_path"
        raw_audio = RawAudio.create(file_path=file_path)
        raw_audio.save()

        raw_audio = RawAudio.get(RawAudio.file_path == file_path)
        assert raw_audio.created_date is not None
