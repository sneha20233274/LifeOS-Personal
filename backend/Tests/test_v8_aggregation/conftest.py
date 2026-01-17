from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from datetime import datetime
from app.models.criteria import Criteria
from app.core.database import Base
import app.models.activity

from app.models.user import User
import pytest
@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")

    # SQLite compatibility for NOW()
    @event.listens_for(engine, "connect")
    def sqlite_now(dbapi_conn, _):
        dbapi_conn.create_function(
            "now",
            0,
            lambda: datetime.utcnow().isoformat(sep=" ")
        )

    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    user = User(
        email_id="test@example.com",
        password_hash="hashed",
        username = "aashu"
    )
    db_session.add(user)
    db_session.commit()
    return user
