from datetime import date, timedelta
from typing import Annotated
from pydantic import BaseModel, Field


# -------- Tool 1: Get today's date --------

class TodayDateOutput(BaseModel):
    today: date = Field(
        ...,
        description="Today's date in YYYY-MM-DD format"
    )


def get_today_date() -> TodayDateOutput:
    """
    Returns today's date.
    """
    return TodayDateOutput(today=date.today())


# -------- Tool 2: Add days to a date --------

class AddDaysInput(BaseModel):
    base_date: date = Field(
        ...,
        description="Base date in YYYY-MM-DD format"
    )
    days: int = Field(
        ...,
        description="Number of days to add (can be positive or negative)"
    )


class AddDaysOutput(BaseModel):
    result_date: date = Field(
        ...,
        description="Resulting date after adding days"
    )


def add_days_to_date(input: AddDaysInput) -> AddDaysOutput:
    """
    Adds a number of days to a given date.
    """
    return AddDaysOutput(
        result_date=input.base_date + timedelta(days=input.days)
    )
