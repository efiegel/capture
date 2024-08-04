class TestDB:
    def test_setup(self, db):
        assert db.is_closed() is False
