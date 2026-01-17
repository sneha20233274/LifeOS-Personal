def compare_values(current: float, previous: float) -> dict:
    """
    Compare two scalar metric values.

    Returns:
    {
        current,
        previous,
        delta,
        trend
    }
    """
    delta = round(current - previous, 3)

    if delta > 0:
        trend = "improving"
    elif delta < 0:
        trend = "declining"
    else:
        trend = "stable"

    return {
        "current": current,
        "previous": previous,
        "delta": delta,
        "trend": trend,
    }

def rolling_average(values: list[float]) -> float:
    """
    Compute rolling average of a metric over time.
    """
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)

def variance(values: list[float]) -> float:
    if not values:
        return 0.0

    mean = sum(values) / len(values)
    return round(
        sum((v - mean) ** 2 for v in values) / len(values),
        3
    )

