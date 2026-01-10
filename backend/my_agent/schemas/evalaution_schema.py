from pydantic import BaseModel

class EvaluatorOutput(BaseModel):
    feedback: str
    approved: bool