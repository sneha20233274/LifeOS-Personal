from pydantic import BaseModel
from my_agent.models.intent import Intent
class IntentResolutionOutput(BaseModel):
    intent: Intent