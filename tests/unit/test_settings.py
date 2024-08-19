class TestSettings:
    def test_setting_with_expanduser_is_none_if_not_set(self, monkeypatch):
        monkeypatch.setenv("SOURCE_AUDIO_DIRECTORY", "")

        from capture.settings import SOURCE_AUDIO_DIRECTORY

        assert SOURCE_AUDIO_DIRECTORY is None
