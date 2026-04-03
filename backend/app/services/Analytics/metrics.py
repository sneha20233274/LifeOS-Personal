from app.models.enums import productive_categories
def compute_productivity(aggregated_by_category: dict) -> float:
    """
    Compute productivity score from aggregated category data.
    Works correctly with Enum or string keys.
    """

    productive_time = 0

    for category, duration in aggregated_by_category.items():
        # ✅ Convert Enum → string safely
        category_str = getattr(category, "value", category)

        if category_str in productive_categories:
            productive_time += duration

    total_time = sum(aggregated_by_category.values())

    if total_time == 0:
        return 0.0

    return round(productive_time / total_time, 3)

def compute_total_time(aggregated_by_category: dict) -> float:
    return sum(aggregated_by_category.values())

