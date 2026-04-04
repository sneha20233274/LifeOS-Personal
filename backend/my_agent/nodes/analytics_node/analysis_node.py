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
# -----------------------------
# 🔥 FORMAT FUNCTION (NEW)
# -----------------------------
def format_aggregation_result(data):
    if data is None:
        return "No activity data found."

    # 🔥 CASE 1: scalar value (float/int)
    if isinstance(data, (int, float)):
        return f"Total time: {round(data, 2)} minutes"

    # 🔥 CASE 2: dictionary
    if isinstance(data, dict):
        if not data:
            return "No activity data found."

        lines = []
        total = 0

        for k, v in data.items():
            key = getattr(k, "value", str(k))
            lines.append(f"- {key}: {round(v, 2)} minutes")
            total += v

        lines.append(f"\nTotal time: {round(total, 2)} minutes")

        return "\n".join(lines)

    # 🔥 fallback
    return str(data)

def analysis_node(state: ChatState) -> ChatState:
    """
    Decides whether to call a tool or provide a final answer.
    It sees the full history, including ToolMessages from the execution node.
    """
    aggregation_result = state.get("aggregation_result", "No data available")
    formatted_data = format_aggregation_result(aggregation_result)
    
    # 1. Inject the Aggregation Result into the System Context
    #    This ensures the LLM sees the data even after looping back from a tool call.
    system_message = SystemMessage(content=f"""
{ANALYSIS_PROMPT}

### USER ACTIVITY DATA
{formatted_data}

---

### INSTRUCTIONS (STRICT)

You MUST follow these rules:

1. The data above is COMPLETE and VALID.
2. NEVER say "data not available".
3. DO NOT ask for more data.
4. Use ONLY the given data.
5. Be direct and clear.

---

### FORMAT RULES (VERY IMPORTANT)

- DO NOT use tables
- DO NOT use "|" symbols
- DO NOT use markdown tables
- Use simple bullet points ONLY
- Keep response clean and readable

---

### RESPONSE STYLE

If showing breakdown:

Example:
You spent your time as follows:
- Work: 4502 minutes
- Learning: 239 minutes
- Exercise: 59 minutes

Total: 5391 minutes (~89.9 hours)

---

If user asks total:

Example:
You spent 5391 minutes (~89.9 hours) this week.

---

If user asks comparison:

Example:
You spent the most time on Work (4502 minutes), followed by Learning (239 minutes).

---

If data is insufficient:

Say:
"I don't have enough data to answer this."

---
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