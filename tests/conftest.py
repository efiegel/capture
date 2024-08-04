import pytest
from peewee import SqliteDatabase

from capture.db import AudioTranscription, RawAudio, database_context

test_db = SqliteDatabase("capture_test.db")


@pytest.fixture(scope="session")
def db():
    with database_context(test_db):
        yield test_db

    test_db.connect()
    test_db.drop_tables([RawAudio, AudioTranscription])
    test_db.close()
