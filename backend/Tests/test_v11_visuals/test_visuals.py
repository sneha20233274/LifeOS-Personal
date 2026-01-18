from app.services.Analytics.visuals import category_distribution,weekday_comparison
from app.models.enums import SummaryCategoryEnum
def test_category_distribution():
    aggregated = {
        SummaryCategoryEnum.learning: 120,
        SummaryCategoryEnum.work: 90,
    }

    result = category_distribution(aggregated)

    assert result["type"] == "category_distribution"
    assert len(result["data"]) == 2
def test_weekday_comparison():
    aggregated = {1: 100, 3: 200}

    result = weekday_comparison(aggregated)

    assert result["type"] == "weekday_comparison"
    assert result["data"][0]["weekday"] == 1
