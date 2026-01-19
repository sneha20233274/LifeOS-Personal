from typing import  Annotated, List, Literal
from pydantic import BaseModel, Field

from typing import Optional, Union, Dict

Int1to10 = Annotated[int, Field(ge=1, le=10)]
Int1to7 = Annotated[int, Field(ge=1, le=7)]
Int0to6 = Annotated[int, Field(ge=0, le=6)]
Int15to180 = Annotated[int, Field(ge=15, le=180)]
Int4to12 = Annotated[int, Field(ge=4, le=12)]


class Intensity(BaseModel):
    level: Literal["low", "moderate", "high"]
    rpe_range: List[Int1to10] = Field(
        min_length=2,
        max_length=2,
        description="RPE range [min, max]"
    )


class WeeklyStructure(BaseModel):
    workout_days: Int1to7
    rest_days: Int0to6


class Recovery(BaseModel):
    sleep_hours: Int4to12
    active_recovery: bool


class FitnessPlan(BaseModel):
    # ---------------- Goal & experience ----------------
    goal: Literal["fat_loss", "muscle_gain", "endurance"]
    experience_level: Literal["beginner", "intermediate", "advanced"]

    # ---------------- Frequency & duration ----------------
    weekly_frequency: Int1to7
    session_duration_min: Int15to180

    # ---------------- Training structure ----------------
    training_split: Literal[
        "full_body",
        "upper_lower",
        "push_pull_legs"
    ]

    workout_types: List[
        Literal["strength", "cardio", "mobility"]
    ]

    # ---------------- Load & recovery ----------------
    intensity: Intensity
    weekly_structure: WeeklyStructure

    # ---------------- Preferences & constraints ----------------
    exercise_preferences: List[str] = Field(default_factory=list)
    exercise_constraints: List[str] = Field(default_factory=list)

    # ---------------- Progression ----------------
    progression_strategy: Literal[
        "linear", "wave", "autoregulatory"
    ]

    recovery: Recovery

    # ---------------- Safety & adherence ----------------
    safety_notes: List[str] = Field(default_factory=list)
    compliance_level: Literal["strict", "flexible"]
 

class StrengthDetails(BaseModel):
    exercise_name: str
    muscle_group: Literal["legs","chest","back","shoulders","biceps","triceps","core", "full_body", "other"]
    sets: int
    reps: int

# ✅ UPDATED: Added "other" and "general"
class CardioDetails(BaseModel):
    activity: Literal["running","cycling","walking","rowing", "general", "other"]
    intensity: Literal["low","moderate","high"]

# ✅ UPDATED: Added "instruction" field for fallback context
class MobilityDetails(BaseModel):
    name: str
    instruction: Optional[str] 

class TimeSlotBlock(BaseModel):
    block_type: Literal["warmup","exercise","break","cooldown","rest"]
    category: Literal["strength","cardio","mobility","none"]
    details: Optional[Union[StrengthDetails, CardioDetails, MobilityDetails]] = None


class DaySchedule(BaseModel):
    day_label: str 
    focus: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    timeline: Dict[str, TimeSlotBlock]

class WeeklyFitnessRoutine(BaseModel):
    routine_id: str
    routine_name: str
    plan_snapshot: FitnessPlan
    schedule: Dict[
        Literal["monday","tuesday","wednesday","thursday","friday","saturday","sunday"],
        DaySchedule
    ]
    created_at: str
    status: Literal["draft","approved"]


class WeeklyFocus(BaseModel):
    monday: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    tuesday: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    wednesday: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    thursday: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    friday: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    saturday: Literal["legs","push","pull","upper","lower","cardio","recovery"]
    sunday: Literal["legs","push","pull","upper","lower","cardio","recovery"]

class TimelineBlockSkeleton(BaseModel):
    start: str        # "07:00"
    end: str          # "07:10"
    block_type: Literal["warmup", "exercise", "break", "cooldown"]
    category: Literal["strength", "cardio", "mobility", "none"]

class DayTimelineSkeleton(BaseModel):
    blocks: List[TimelineBlockSkeleton]

