import pytest
from unittest.mock import MagicMock, patch
from datetime import date
from app.models.enums import SummaryCategoryEnum

# Tools under test
from my_agent.tools.analytics_tools import (
    check_execution_quality,
    get_criteria_breakdown,
    analyze_activities,
    calculate_productivity_score,
    calculate_total_time,
    analyze_trend,
    calculate_variance,
    calculate_average,
)

# -------------------------------------------------------------------------
# DATABASE-BACKED TOOLS
# -------------------------------------------------------------------------

@patch("my_agent.tools.analytics_tools.execution_quality")
@patch("my_agent.tools.analytics_tools.get_db")
def test_check_execution_quality(mock_get_db, mock_service):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_service.return_value = {"completion_ratio": 0.8}

    result = check_execution_quality.func(
        user_id=1,
        start_date="2023-10-01",
        end_date="2023-10-07",
    )

    assert result == {"completion_ratio": 0.8}

    mock_service.assert_called_once_with(
        mock_db,
        1,
        date(2023, 10, 1),
        date(2023, 10, 7),
    )


@patch("my_agent.tools.analytics_tools.criteria_breakdown")
@patch("my_agent.tools.analytics_tools.get_db")
def test_get_criteria_breakdown(mock_get_db, mock_service):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_service.return_value = {"Deep Work": 120}

    result = get_criteria_breakdown.func(
        user_id=1,
        start_date="2023-01-01",
        end_date="2023-01-02",
    )

    assert result == {"Deep Work": 120}

    mock_service.assert_called_once_with(
        mock_db,
        1,
        date(2023, 1, 1),
        date(2023, 1, 2),
    )


@patch("my_agent.tools.analytics_tools.aggregate_activities")
@patch("my_agent.tools.analytics_tools.get_db")
def test_analyze_activities(mock_get_db, mock_aggregate):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_aggregate.return_value = {"work": 100.0}

    result = analyze_activities.func(
        user_id=1,
        start_date="2023-01-01",
        end_date="2023-01-31",
        group_by="summary_category",
        aggregation_type="sum",
    )

    assert result == {"work": 100.0}

    args, _ = mock_aggregate.call_args
    db_arg, filters_arg, spec_arg = args

    assert db_arg is mock_db
    assert filters_arg.date_range.start == date(2023, 1, 1)
    assert filters_arg.date_range.end == date(2023, 1, 31)
    assert spec_arg.group_by == "summary_category"
    assert spec_arg.aggregation == "sum"


# -------------------------------------------------------------------------
# PURE METRIC / MATH TOOLS (NO DB)
# -------------------------------------------------------------------------

@patch("my_agent.tools.analytics_tools.compute_productivity")
def test_calculate_productivity_score(mock_compute):
    mock_compute.return_value = 0.75

    input_data = {
        SummaryCategoryEnum.work: 120.0,
        SummaryCategoryEnum.leisure: 30.0,
    }

    result = calculate_productivity_score.func(input_data)

    assert result == 0.75

    mock_compute.assert_called_once_with(
        {"work": 120.0, "leisure": 30.0}
    )


@patch("my_agent.tools.analytics_tools.compute_total_time")
def test_calculate_total_time(mock_compute):
    mock_compute.return_value = 150.0

    result = calculate_total_time.func(
        {"work": 100.0, "gym": 50.0}
    )

    assert result == 150.0

    mock_compute.assert_called_once_with(
        {"work": 100.0, "gym": 50.0}
    )


@patch("my_agent.tools.analytics_tools.compare_values")
def test_analyze_trend(mock_compare):
    mock_compare.return_value = {"delta": 10, "trend": "improving"}

    result = analyze_trend.func(100.0, 90.0)

    assert result == {"delta": 10, "trend": "improving"}

    mock_compare.assert_called_once_with(100.0, 90.0)


@patch("my_agent.tools.analytics_tools.variance")
def test_calculate_variance(mock_var):
    mock_var.return_value = 5.0

    result = calculate_variance.func([1, 2, 3])

    assert result == 5.0
    mock_var.assert_called_once_with([1, 2, 3])


@patch("my_agent.tools.analytics_tools.rolling_average")
def test_calculate_average(mock_avg):
    mock_avg.return_value = 2.0

    result = calculate_average.func([1, 2, 3])

    assert result == 2.0
    mock_avg.assert_called_once_with([1, 2, 3])
