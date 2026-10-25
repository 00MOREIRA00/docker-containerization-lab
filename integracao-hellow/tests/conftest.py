import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

os.environ.setdefault("POSTGRES_PASSWORD", "test-password")

from provider.database import Base  # noqa: E402


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)

    try:
        yield session
    finally:
        session.close()
        engine.dispose()
