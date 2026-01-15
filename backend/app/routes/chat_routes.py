from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.run_chat_controller import run_chat
from app.controllers.resume_chat_controller import resume_chat_controller
from app.controllers.create_new_chat_controller import create_new_chat_controller
from app.core.database import get_db

router = APIRouter(
   
    tags=["Chat"]
)

DEFAULT_USER_ID = 1

@router.post("/run")
def run_chat_route(
    request: dict,
    db: Session = Depends(get_db),
):
    return run_chat(
        request=request,
        db=db,
        user_id=DEFAULT_USER_ID
    )

@router.post("/resume")
def resume_chat_route(
    request: dict,
    db: Session = Depends(get_db),
):
    return resume_chat_controller(
        request=request,
        db=db,
    )

@router.post("/new")
def new_chat_route():
    return create_new_chat_controller(user_id=DEFAULT_USER_ID)
