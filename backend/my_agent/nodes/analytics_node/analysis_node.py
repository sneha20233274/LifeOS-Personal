# nodes/analytics/analysis_node.py
from langchain_core.messages import SystemMessage, HumanMessage
from my_agent.chatstate import ChatState
from my_agent.llm import analysis_llm
from my_agent.prompts.analytics_prompt import ANALYSIS_PROMPT

from my_agent.tools.analytics_tools import (
    calculate_total_time,
    check_execution_quality,
    get_criteria_breakdown,
    calculate_productivity_score,
    calculate_average,
    analyze_trend,
    calculate_variance,
    calculate_average
)
tools = [
    calculate_total_time,
    calculate_productivity_score,
    calculate_average,
    analyze_trend,
    calculate_variance,
    calculate_average]
tools_by_name = {tool.name: tool for tool in tools}

analysis_llm_model = analysis_llm.bind_tools( tools )

def analysis_node(state: ChatState) -> ChatState:
    """
    Decides whether to call a tool or provide a final answer.
    It sees the full history, including ToolMessages from the execution node.
    """
    aggregation_result = state.get("aggregation_result", "No data available")
    
    # 1. Inject the Aggregation Result into the System Context
    #    This ensures the LLM sees the data even after looping back from a tool call.
    system_message = SystemMessage(content=f"""
{ANALYSIS_PROMPT}

### CURRENT DATA CONTEXT
The following data has been retrieved based on the user's query:
{aggregation_result}

Use this data to answer the user or use tools to calculate specific metrics.
""")

    # 2. Combine System Prompt with Conversation History
    #    state["messages"] contains the User query + previous AI tool calls + Tool outputs
    messages = [system_message] + state["messages"]

    # 3. Invoke the LLM
    response = analysis_llm_model.invoke(messages)

    # 4. Return the response
    #    We do NOT execute tools here. We just return the AIMessage.
    #    The graph's 'should_continue' edge will detect the tool_calls 
    #    and route to 'tool_node_analytics'.
    return {"messages": [response]}