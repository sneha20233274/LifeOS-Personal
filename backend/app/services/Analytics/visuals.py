def category_distribution(aggregated: dict) -> dict:
    """
    Converts:
    {category: value}
    →
    chart-friendly category distribution
    """

    return {
        "type": "category_distribution",
        "data": [
            {"label": str(category), "value": round(value, 2)}
            for category, value in aggregated.items()
        ]
    }
def weekday_comparison(aggregated: dict) -> dict:
    """
    Converts:
    {weekday_int: value}
    →
    bar chart data
    """

    return {
        "type": "weekday_comparison",
        "data": [
            {"weekday": int(day), "value": round(value, 2)}
            for day, value in sorted(aggregated.items())
        ]
    }
def time_series(metric_name: str, series: list[tuple]) -> dict:
    """
    Input:
    [
        (date, value),
        ...
    ]
    """

    return {
        "type": "time_series",
        "metric": metric_name,
        "data": [
            {"date": d.isoformat(), "value": round(v, 3)}
            for d, v in series
        ]
    }
