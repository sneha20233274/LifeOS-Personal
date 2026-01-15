import datetime
from pydantic import BaseModel
from enum import Enum

def normalize_payload(obj):
    if isinstance(obj, BaseModel):
        return normalize_payload(obj.model_dump())

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, dict):
        return {k: normalize_payload(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [normalize_payload(v) for v in obj]

    if isinstance(obj, datetime.date):
        return obj.isoformat()

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()

    return obj
