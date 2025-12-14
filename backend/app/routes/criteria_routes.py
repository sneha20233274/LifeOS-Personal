from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from models.criteria import Criteria
from schemas.activity import CriteriaOut

router = APIRouter( tags=["criteria"])


@router.get("/", response_model=List[CriteriaOut], summary="Get all criteria")
def get_criteria(db: Session = Depends(get_db)):
    """
    Returns all predefined criteria.
    Frontend uses this to render selection UI.
    """
    return (
        db.query(Criteria)
        .order_by(Criteria.name.asc())
        .all()
    )
