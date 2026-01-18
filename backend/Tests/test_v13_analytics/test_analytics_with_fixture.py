import pytest
from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from app.core.database import Base
from app.models.enums import SummaryCategoryEnum
from app.models.activity import Activity

from my_agent.tools.analytics_tools import (
    analyze_activities,
    get_criteria_breakdown,
    check_execution_quality,
    calculate_productivity_score,
    calculate_total_time,
    analyze_trend,
    calculate_variance,
    calculate_average,
)

# -------------------------------------------------------------------------
# SQLITE DB FIXTURE (USED ONLY WHERE IT MAKES SENSE)
# -------------------------------------------------------------------------

@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def sqlite_now(dbapi_conn, _):
        dbapi_conn.create_function(
            "now",
            0,
            lambda: datetime.utcnow().isoformat(sep=" ")
        )

    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# -------------------------------------------------------------------------
# AGGREGATION TOOL (REAL INTEGRATION TEST)
# -------------------------------------------------------------------------

@patch("my_agent.tools.analytics_tools.get_db")
def test_analyze_activities_with_sqlite(mock_get_db, db):
    mock_get_db.return_value = db

    activity = Activity(
        user_id=1,
        summary_category=SummaryCategoryEnum.work,
        duration_minutes=120,
        start_ts=datetime(2023, 1, 10, 9, 0),
    )
    db.add(activity)
    db.commit()

    result = analyze_activities.func(
        user_id=1,
        start_date="2023-01-01",
        end_date="2023-01-31",
        group_by="summary_category",
        aggregation_type="sum",
    )

    assert result == {SummaryCategoryEnum.work: 120.0}


# -------------------------------------------------------------------------
# SERVICE-LEVEL TOOLS (MOCKED — BY DESIGN)
# -------------------------------------------------------------------------

@patch("my_agent.tools.analytics_tools.criteria_breakdown")
@patch("my_agent.tools.analytics_tools.get_db")
def test_get_criteria_breakdown(mock_get_db, mock_service, db):
    mock_get_db.return_value = db
    mock_service.return_value = {"Deep Work": 120}

    result = get_criteria_breakdown.func(
        user_id=1,
        start_date="2023-01-01",
        end_date="2023-01-31",
    )

    assert result == {"Deep Work": 120}
    mock_service.assert_called_once()


@patch("my_agent.tools.analytics_tools.execution_quality")
@patch("my_agent.tools.analytics_tools.get_db")
def test_check_execution_quality(mock_get_db, mock_service, db):
    mock_get_db.return_value = db
    mock_service.return_value = {"completion_ratio": 0.9}

    result = check_execution_quality.func(
        user_id=1,
        start_date="2023-01-01",
        end_date="2023-01-31",
    )

    assert result == {"completion_ratio": 0.9}
    mock_service.assert_called_once()


# -------------------------------------------------------------------------
# PURE METRIC / MATH TOOLS (NO DB)
# -------------------------------------------------------------------------

def test_calculate_productivity_score():
    data = {
        SummaryCategoryEnum.work: 120.0,
        SummaryCategoryEnum.leisure: 30.0,
    }
    result = calculate_productivity_score.func(data)
    assert 0 <= result <= 1


def test_calculate_total_time():
    result = calculate_total_time.func({"work": 100.0, "gym": 50.0})
    assert result == 150.0


def test_analyze_trend():
    result = analyze_trend.func(100.0, 90.0)
    assert result["trend"] == "improving"


def test_calculate_variance():
    result = calculate_variance.func([1, 2, 3])
    assert isinstance(result, float)


def test_calculate_average():
    result = calculate_average.func([1, 2, 3])
    assert result == 2.0
