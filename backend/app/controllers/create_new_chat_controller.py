from uuid import uuid4
from sqlalchemy.orm import Session

def create_new_chat_controller(user_id: int, db: Session):
    thread_id = str(uuid4())

    # later you can persist using db
    # db.add(...)
    # db.commit()

    return {
        "thread_id": thread_id
    }
