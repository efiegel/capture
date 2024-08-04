import pytest
from peewee import SqliteDatabase

from capture.db import all_models, database_context

test_db = SqliteDatabase("capture_test.db")


@pytest.fixture(scope="session", autouse=True)
def db():
    with database_context(test_db):
        yield test_db

    test_db.connect()
    test_db.drop_tables(all_models)
    test_db.close()
