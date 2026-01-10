from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


# ---------- Read ----------

class ProposalRead(BaseModel):
    proposal_id: int
    run_id: str
    action_type: str
    payload: Dict[str, Any]
    status: str
    version: int
    reason: Optional[str]

    class Config:
        from_attributes = True


# ---------- Update (EDITABLE PAYLOAD ONLY) ----------

class ProposalUpdate(BaseModel):
    payload: Dict[str, Any] = Field(
        ...,
        description="Editable payload only. action_type cannot be changed."
    )


# ---------- Approval ----------

class ProposalApprove(BaseModel):
    comment: Optional[str] = None


class ProposalReject(BaseModel):
    comment: Optional[str] = None
