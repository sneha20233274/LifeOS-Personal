from langchain_core.messages import HumanMessage
from my_agent.chatstate import ChatState
from my_agent.model_gen import chatbot 


def test_task_structure_generation_end_to_end():
    """
    Integration test:
    - User gives a task creation prompt
    - LangGraph runs end-to-end
    - Tasks and subtasks are produced
    """
    thread_id = "thread"

    # ---------------- STEP 1: START AGENT (INTERRUPT) ----------------
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    final_state = chatbot.invoke(
        {
            "messages": [HumanMessage(content="Create a task to complete agentic AI project in 10 days")],
            "iteration": 0,
            "max_iterations": 1,
        },
        config=config
    )
    

    

    # Basic sanity assertions
    
    assert len(final_state["routine_tasks"]) > 0

    # Validate structure shape
    print("Generated Tasks and Subtasks:", final_state["routine_tasks"])
