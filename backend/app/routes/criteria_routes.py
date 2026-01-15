from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.criteria import Criteria
from app.schemas.activity import CriteriaOut
from app.utils.oauth2_scheme  import swagger_bearer_auth
router = APIRouter( tags=["criteria"], dependencies=[Depends(swagger_bearer_auth)])


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
