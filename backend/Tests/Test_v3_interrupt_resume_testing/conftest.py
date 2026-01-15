from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.subtask import Subtask
from my_agent.models.action_proposal import ActionProposal
from app.models.criteria import Criteria
from sqlalchemy import event
from datetime import datetime

from app.core.database import Base
from app.models.subtask import Subtask, SubtaskType
from my_agent.models.action_proposal import ActionProposal, ProposalStatus
import pytest
@pytest.fixture()
def db():
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