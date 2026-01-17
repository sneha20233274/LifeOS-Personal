from app.services.Analytics.comparison import compare_values,rolling_average,variance
def test_compare_improving():
    result = compare_values(0.72, 0.65)

    assert result == {
        "current": 0.72,
        "previous": 0.65,
        "delta": 0.07,
        "trend": "improving",
    }
def test_compare_declining():
    result = compare_values(0.60, 0.72)

    assert result["trend"] == "declining"
    assert result["delta"] == -0.12
def test_compare_stable():
    result = compare_values(0.7, 0.7)

    assert result["trend"] == "stable"
    assert result["delta"] == 0.0
def test_rolling_average():
    values = [0.6, 0.7, 0.8]

    result = rolling_average(values)

    assert result == 0.7

def test_variance():
    values = [0.6, 0.7, 0.8]

    result = variance(values)

    assert result > 0

