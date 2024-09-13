import importlib

from capture import settings


class TestSettings:
    def test_setting_with_expanduser_is_none_if_not_set(self, monkeypatch):
        monkeypatch.setenv("AUDIO_DIRECTORY", "")
        importlib.reload(settings)
        assert settings.AUDIO_DIRECTORY is None
