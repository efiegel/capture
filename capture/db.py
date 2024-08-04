from contextlib import contextmanager
from datetime import datetime
from uuid import uuid4

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

db = SqliteDatabase("capture.db")


@contextmanager
def database_context(database: SqliteDatabase = db):
    try:
        database.connect()
        database.bind(
            [RawAudio, AudioTranscription], bind_refs=False, bind_backrefs=False
        )
        database.create_tables([RawAudio, AudioTranscription])
        yield database
    finally:
        if not database.is_closed():
            database.close()


class BaseModel(Model):
    class Meta:
        database = None


class RawAudio(BaseModel):
    file_path = CharField(primary_key=True)
    created_date = DateTimeField(default=datetime.now)


class AudioTranscription(BaseModel):
    file_path = CharField(primary_key=True, default=lambda: str(uuid4()))
    raw_audio = ForeignKeyField(RawAudio, backref="transcriptions")
    model = CharField()
    transcription_time_seconds = IntegerField()
    created_at = DateTimeField(default=datetime.now)
