"""Memory Database Test configuration"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    in_memory_db_engine = create_engine("sqlite:///:memory:")
    metadata.create_all(in_memory_db_engine)

    return in_memory_db_engine


@pytest.fixture
def session(in_memory_db):  # pylint: disable=redefined-outer-name
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
