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
def database_context():
    try:
        db.connect()
        db.create_tables([RawAudio, AudioTranscription])
        yield db
    finally:
        if not db.is_closed():
            db.close()


class BaseModel(Model):
    class Meta:
        database = db


class RawAudio(BaseModel):
    file_path = CharField(primary_key=True)
    created_date = DateTimeField(default=datetime.now)


class AudioTranscription(BaseModel):
    file_path = CharField(primary_key=True, default=lambda: str(uuid4()))
    raw_audio = ForeignKeyField(RawAudio, backref="transcriptions")
    model = CharField()
    transcription_time_seconds = IntegerField()
    created_at = DateTimeField(default=datetime.now)
