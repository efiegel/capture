from contextlib import contextmanager
from datetime import datetime

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
        database.bind(all_models, bind_refs=False, bind_backrefs=False)
        database.create_tables(all_models)
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
    file_path = CharField(primary_key=True)
    raw_audio = ForeignKeyField(RawAudio, backref="transcriptions")
    model = CharField()
    transcription_time_seconds = IntegerField()
    created_at = DateTimeField(default=datetime.now)


all_models = [RawAudio, AudioTranscription]
