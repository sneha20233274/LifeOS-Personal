AGG_PROMPT = """
Decide whether aggregation is required.

If aggregation is required:
- Output an object matching AggregationSpec

If aggregation is NOT required:
- Output: { "type": "none" }

Rules:
- Output ONLY JSON
- Do NOT explain
- Do NOT compute
"""

ANALYSIS_PROMPT = """
You analyze precomputed aggregation results.

You MAY call tools to:
- compute metrics
- compare values

Rules:
- Do NOT compute manually
- Do NOT invent numbers
- Use tools if needed
"""
