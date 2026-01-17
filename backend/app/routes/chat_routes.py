from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.run_chat_controller import run_chat
from app.controllers.resume_chat_controller import resume_chat_controller
from app.controllers.create_new_chat_controller import create_new_chat_controller
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    
    tags=["Chat"]
)

@router.post("/run")
def run_chat_route(
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return run_chat(
        request=request,
        db=db,
        user_id=current_user.user_id
    )

@router.post("/resume")
def resume_chat_route(
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resume_chat_controller(
        request=request,
        db=db,
        user_id=current_user.user_id,
    )
@router.post("/new")
def new_chat_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("CHAT NEW ROUTE HIT")
    print("USER:", current_user)
    return create_new_chat_controller(
        user_id=current_user.user_id,
        db=db
    )
