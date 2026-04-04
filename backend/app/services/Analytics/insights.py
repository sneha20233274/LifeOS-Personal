from app.services.Analytics.comparison import compare_values, variance
from app.services.Analytics.metrics import compute_productivity
from app.models.enums import SummaryCategoryEnum

PRODUCTIVE = {"work", "learning", "exercise"}


def _clean_category(category):
    return getattr(category, "value", str(category))


def generate_insights(category_data, weekday_data, productivity_trend):
    insights = []

    # -----------------------------
    # Normalize category keys
    # -----------------------------
    category_data = {
        _clean_category(k): v for k, v in category_data.items()
    }

    # -----------------------------
    # 1. MOST PRODUCTIVE CATEGORY
    # -----------------------------
    if category_data:
        best_cat = max(category_data, key=category_data.get)

        insights.append({
            "type": "positive",
            "text": f"You spent most time on {best_cat}"
        })

    # -----------------------------
    # 2. TIME WASTE DETECTION (FIXED)
    # -----------------------------
    waste_categories = {
        k: v for k, v in category_data.items()
        if k not in PRODUCTIVE
    }

    if waste_categories:
        worst = max(waste_categories, key=waste_categories.get)

        insights.append({
            "type": "warning",
            "text": f"High time spent on {worst}. Consider reducing it."
        })

    # -----------------------------
    # 3. BEST DAY
    # -----------------------------
    if weekday_data:
        best_day = max(weekday_data, key=weekday_data.get)

        insights.append({
            "type": "positive",
            "text": f"You perform best on day {int(best_day)}"
        })

    # -----------------------------
    # 4. TREND (FIXED ICON ISSUE)
    # -----------------------------
    if len(productivity_trend) >= 2:
        trend = compare_values(
            productivity_trend[-1],
            productivity_trend[0]
        )

        if trend["trend"] == "improving":
            insights.append({
                "type": "positive",
                "text": f"Productivity improving by {trend['delta']:.2f}"
            })
        elif trend["trend"] == "declining":
            insights.append({
                "type": "warning",
                "text": f"Productivity declining by {abs(trend['delta']):.2f}"
            })
        else:
            insights.append({
                "type": "neutral",
                "text": "Your productivity is stable"
            })

    # -----------------------------
    # 5. CONSISTENCY
    # -----------------------------
    if productivity_trend:
        var = variance(productivity_trend)

        if var < 3:
            insights.append({
                "type": "positive",
                "text": "You are highly consistent"
            })
        elif var < 10:
            insights.append({
                "type": "neutral",
                "text": "Moderate consistency in your routine"
            })
        else:
            insights.append({
                "type": "warning",
                "text": "Your routine is inconsistent"
            })

    # -----------------------------
    # 6. PRODUCTIVITY SCORE INSIGHT
    # -----------------------------
    productivity = compute_productivity(category_data)

    if productivity > 0.7:
        insights.append({
            "type": "positive",
            "text": "Excellent productivity level"
        })
    elif productivity > 0.4:
        insights.append({
            "type": "neutral",
            "text": "Decent productivity, room for improvement"
        })
    else:
        insights.append({
            "type": "warning",
            "text": "Low productivity, focus on high-value tasks"
        })

    # -----------------------------
    # 7. BALANCE INSIGHT (NEW 🔥)
    # -----------------------------
    if category_data:
        total = sum(category_data.values())

        top = max(category_data.values())
        ratio = top / total if total else 0

        if ratio > 0.6:
            insights.append({
                "type": "warning",
                "text": "Too much time concentrated in one area"
            })
        else:
            insights.append({
                "type": "positive",
                "text": "Good balance across activities"
            })

    return insights