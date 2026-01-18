# nodes/analytics/aggregation_node.py
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from my_agent.chatstate import ChatState
from my_agent.llm import analytics_structured_llm
from my_agent.schemas.analytics import AggregationOutput, AggregationSpec
from my_agent.prompts.analytics_prompt import AGG_PROMPT
from app.services.Analytics.aggregation import aggregate_activities
from app.core.database import get_db
from app.services.Analytics.primitives import ActivityFilters, DateRange
from datetime import date


def aggregation_node(state: ChatState, config: RunnableConfig) -> ChatState:
    user_query = state["messages"][-1].content
    configuration = config.get("configurable", {})
    current_user_id = configuration.get("user_id")

    messages = [
        SystemMessage(content=AGG_PROMPT),
        HumanMessage(content=user_query),
    ]

    # 🔹 Structured LLM call
    output: AggregationOutput = analytics_structured_llm.invoke(messages)

    # -----------------------------
    # Case 1: No aggregation needed
    # -----------------------------
    if output.type == "none":
        state["aggregation_spec"] = None
        state["aggregation_result"] = None
        return state

    # -----------------------------
    # Case 2: Aggregation required
    # -----------------------------
    if output.aggregation is None:
        raise ValueError(
            "AggregationOutput.type='aggregation' but aggregation is None"
        )

    spec: AggregationSpec = output.aggregation

    # -----------------------------
    # Build ActivityFilters
    # -----------------------------
    filters = ActivityFilters(
        date_range=DateRange(
            start=spec.date_range.start,
            end=spec.date_range.end,
        ),
        day_of_week=spec.day_of_week,
        summary_category=spec.summary_category,
    )

    # -----------------------------
    # Execute aggregation
    # -----------------------------
    db = next(get_db())
    result = aggregate_activities(
        db=db,
        user_id=current_user_id,
        filters=filters,
        spec=spec,
    )

    # -----------------------------
    # Persist in state
    # -----------------------------
    state["aggregation_spec"] = spec.model_dump()
    state["aggregation_result"] = result

    return state
