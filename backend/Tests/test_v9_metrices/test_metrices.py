from app.services.Analytics.metrics import compute_productivity,compute_total_time
from app.models.enums import SummaryCategoryEnum
def test_compute_productivity_normal_case():
    aggregated = {
        SummaryCategoryEnum.learning: 120,
        SummaryCategoryEnum.work: 90,
        SummaryCategoryEnum.leisure: 30,
    }

    result = compute_productivity(aggregated)
    result1 = compute_total_time(aggregated)

    assert result == 0.875
    assert result1 == 240
def test_compute_productivity_all_productive():
    aggregated = {
        SummaryCategoryEnum.learning: 100,
        SummaryCategoryEnum.work: 100,
    }

    result = compute_productivity(aggregated)

    assert result == 1.0
def test_compute_productivity_none_productive():
    aggregated = {
        SummaryCategoryEnum.leisure: 120,
        SummaryCategoryEnum.health: 60,
    }

    result = compute_productivity(aggregated)

    assert result == 0.0
def test_compute_productivity_zero_time():
    aggregated = {}

    result = compute_productivity(aggregated)

    assert result == 0.0
