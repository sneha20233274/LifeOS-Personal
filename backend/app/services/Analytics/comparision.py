def compare_values(current: float, previous: float) -> dict:
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
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)
