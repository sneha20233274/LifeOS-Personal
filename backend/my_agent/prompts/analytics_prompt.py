AGG_PROMPT = """
Decide whether aggregation is required.

Today's date is: {today}

If aggregation is required:
- Output an object matching AggregationSpec

Date Rules (VERY IMPORTANT):
- ALWAYS use today's date as reference
- If user says:
  - "last X days" → end = today, start = today - X days
  - "past X days" → same as above
  - "X days ago" → start = today - X, end = today - X + 1
  - "this week" → use current week
  - "this month" → use current month
- If user gives NO date → default to last 7 days

- Dates MUST be real ISO dates (YYYY-MM-DD)
- Do NOT output years like 2023 unless explicitly asked

If aggregation is NOT required:
- Output: {{ "type": "none" }}

Rules:
- Output ONLY JSON
- Do NOT explain
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

FORMAT RULES:
- NEVER use markdown tables
- NEVER use pipes (|)
- Use clean bullet points
- Keep output simple and readable

Example:
You spent:
- Work: 4502 minutes
- Learning: 239 minutes
- Exercise: 59 minutes

Total: 5391 minutes (~89.9 hours)
"""
