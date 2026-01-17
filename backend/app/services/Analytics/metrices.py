from app.models.enums import productive_categories
def compute_productivity(aggregated_by_category: dict[str, float]) -> float:
    productive_time = sum(
        duration
        for category, duration in aggregated_by_category.items()
        if category in productive_categories
    )

    total_time = sum(aggregated_by_category.values())

    if total_time == 0:
        return 0.0

    return round(productive_time / total_time, 3)
