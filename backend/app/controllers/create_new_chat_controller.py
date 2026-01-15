from uuid import uuid4

def create_new_chat_controller(user_id: int):
    """
    Creates a new chat session (thread).
    """
    thread_id = str(uuid4())

    # OPTIONAL (recommended):
    # save chat session metadata to DB
    # ChatSession(thread_id=thread_id, user_id=user_id)

    return {
        "thread_id": thread_id
    }
