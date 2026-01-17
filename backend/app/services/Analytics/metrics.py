from app.models.enums import productive_categories
def compute_productivity(aggregated_by_category: dict[str, float]) -> float:
    """
      Compute productivity score from aggregated category data.

      Input example:
      {
          SummaryCategoryEnum.learning: 120,
          SummaryCategoryEnum.work: 90,
          SummaryCategoryEnum.leisure: 30,
      }

      Output:
      0.7
    """
    productive_time = sum(
        duration
        for category, duration in aggregated_by_category.items()
        if category in productive_categories
    )

    total_time = sum(aggregated_by_category.values())

    if total_time == 0:
        return 0.0

    return round(productive_time / total_time, 3)

def compute_total_time(aggregated_by_category: dict) -> float:
    return sum(aggregated_by_category.values())

