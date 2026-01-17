# backend/app/models/enums.py
import enum

class SummaryCategoryEnum(str, enum.Enum):
    work = "work"
    learning = "learning"
    exercise = "exercise"
    admin = "admin"
    leisure = "leisure"
    sleep = "sleep"
    social = "social"
    commute = "commute"
    other = "other"


#productive categories
productive_categories = {
    SummaryCategoryEnum.work,
    SummaryCategoryEnum.learning,
    SummaryCategoryEnum.exercise,
    SummaryCategoryEnum.admin,
}
