from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from typing import List,Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.schemas.routine_event import (
    RoutineEventCreate,
    RoutineEventUpdate,
    RoutineEventResponse
)
from app.services.routine_event import (
    create_routine_event,
    list_routine_events,
    get_routine_event,
    update_routine_event,
    delete_routine_event,
    list_routine_events_by_date, 
)
from app.models.user import User
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter( tags=["Events"])


@router.post("", response_model=RoutineEventResponse)
def create_event(
    payload: RoutineEventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    print("create")
    print(payload)
    return create_routine_event(db, user.user_id, payload)


@router.get("", response_model=List[RoutineEventResponse])
def list_events(
    date: Optional[str] = Query(None),
    tz: Optional[str] = Query("UTC"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    if date:
        parsed_date = datetime.fromisoformat(date.replace("Z", "+00:00"))

        r = list_routine_events_by_date(
            db=db,
            user_id=user.user_id,
            date=parsed_date,
            tz=tz,
        )
        print (r)
        return r

    return list_routine_events(db, user.user_id)


@router.get("/{event_id}", response_model=RoutineEventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_routine_event(db, user.user_id, event_id)


@router.put("/{event_id}", response_model=RoutineEventResponse)
def update_event(
    event_id: int,
    payload: RoutineEventUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return update_routine_event(db, user.user_id, event_id, payload)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    print("delet")
    delete_routine_event(db, user.user_id, event_id)
    return {"success": True}


