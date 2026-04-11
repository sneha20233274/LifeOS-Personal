from sqlalchemy.orm import Session
from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from my_agent.model_gen import chatbot
from langchain_core.messages import AIMessage, HumanMessage

from my_agent.models.action_proposal import ActionProposal, ProposalStatus
from app.services.Executor.dispatcher import execute_proposals

from datetime import datetime


# ✅ HELPER: convert datetime → string
def serialize_payload(payload: dict):
    new_payload = {}

    for k, v in payload.items():
        if isinstance(v, datetime):
            new_payload[k] = v.isoformat()
        else:
            new_payload[k] = v

    return new_payload


def run_chat(request: dict, db: Session, user_id: int):
    try:
        prompt = request["prompt"]
        thread_id = request.get("thread_id")

        if not thread_id:
            raise ValueError("thread_id is required")

        # ✅ IMPORTANT: DO NOT PASS DB HERE
        # ✅ CORRECT
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
                "db": db   # 🔥 ADD THIS
            }
        }

        # 🔥 CALL AGENT
        result = chatbot.invoke(
            {
                "messages": [HumanMessage(content=prompt)],
                "iteration": 0,
                "max_iterations": 5,
            },
            config=config,
        )

        # 🔍 DEBUG (safe)
        print("🔍 Agent result:", result)

        intent = result.get("intent")

        # =====================================================
        # 🔥 AUTO EXECUTE FOR ROUTINE (NO APPROVAL)
        # =====================================================
        if intent == "scheduling":
            raw_proposals = result.get("proposals", [])

            db_proposals = []

            for p in raw_proposals:
                clean_payload = serialize_payload(p["payload"])

                proposal = ActionProposal(
                    user_id=user_id,
                    thread_id=thread_id,
                    action_type=p["action_type"],
                    payload=clean_payload,
                    status=ProposalStatus.APPROVED
                )

                db.add(proposal)
                db.flush()
                db_proposals.append(proposal)

            # 🔥 EXECUTE IMMEDIATELY
            execution_result = execute_proposals(db, db_proposals)

            print("✅ Routine execution:", execution_result)

            return {
                "status": "COMPLETED",
                "thread_id": thread_id,
                "messages": [
                    {
                        "content": "✨ Your daily routine is ready! Opening DayCraft..."
                    }
                ],
                "redirect": "/calender"
            }

        # =====================================================
        # 🔵 NORMAL FLOW (GOAL / ACTIVITY → NEED APPROVAL)
        # =====================================================
        if "__interrupt__" in result:
            proposals_data = result.get("proposals", [])

            print("🟡 Proposals received:", proposals_data)

            saved_proposals = save_proposals(
                db=db,
                thread_id=thread_id,
                user_id=user_id,
                proposals=proposals_data,
            )

            apply_dependencies(db, saved_proposals)

            return {
                "status": "WAITING_FOR_APPROVAL",
                "thread_id": thread_id,
                "proposals": [
                    {
                        "proposal_id": p.proposal_id,
                        "action_type": p.action_type,
                        "status": p.status.name,
                        "payload": p.payload or {},
                    }
                    for p in saved_proposals
                ],
            }

        # =====================================================
        # 🟢 NORMAL AI RESPONSE
        # =====================================================
        final_messages = result.get("messages", [])

        last_ai_message = None
        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage) and msg.content:
                last_ai_message = msg
                break

        if last_ai_message:
            return {
                "status": "COMPLETED",
                "thread_id": thread_id,
                "messages": [
                    {"content": last_ai_message.content}
                ],
            }

        # fallback
        return {
            "status": "COMPLETED",
            "thread_id": thread_id,
            "messages": [
                {"content": "I couldn't generate a response."}
            ],
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        print("💥 ERROR IN run_chat:", str(e))

        return {
            "status": "ERROR",
            "thread_id": request.get("thread_id"),
            "messages": [
                {
                    "content": f"Something went wrong: {str(e)}"
                }
            ],
        }