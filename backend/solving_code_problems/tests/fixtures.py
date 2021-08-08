import pytest


@pytest.fixture(autouse=True)
def use_db(db):
    pass
