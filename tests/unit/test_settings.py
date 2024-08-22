import importlib

from capture import settings


class TestSettings:
    def test_setting_with_expanduser_is_none_if_not_set(self, monkeypatch):
        monkeypatch.setenv("SOURCE_AUDIO_DIRECTORY", "")
        importlib.reload(settings)
        assert settings.SOURCE_AUDIO_DIRECTORY is None
