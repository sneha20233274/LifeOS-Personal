from langchain_core.messages import HumanMessage
from langgraph.types import Command
import pprint
from app.core.database import get_db
from my_agent.model_gen import chatbot


from app.models.criteria import Criteria


def test_task_structure_generation_end_to_end():
   
    thread_id = "threadz"
    user_id = 5,
    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id,
        }
    }
    print("Invoking chatbot...")
    final_state = chatbot.invoke(
        {
            "messages": [
                HumanMessage(
                    content="i want to know time i have spend on various type of activity in past one month"
                )
            ],
            "iteration": 0,
            "max_iterations": 1,
            
        },
        config=config
    )

    pprint.pprint(final_state)

    
if __name__ == "__main__":
    test_task_structure_generation_end_to_end()
