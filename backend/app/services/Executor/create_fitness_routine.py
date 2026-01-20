# app/services/Executor/fitness_routine.py
from sqlalchemy.orm import Session
from app.models.weekly_fitness_routine import WeeklyFitnessRoutineDB
from app.models.fitness_timeline_block import FitnessTimelineBlockDB
import uuid


class CreateFitnessRoutineExecutor:
    def execute(self, db: Session, proposal, all_proposals):
        payload = proposal.payload
        user_id = proposal.user_id

        # 1️⃣ Store routine (SOURCE OF TRUTH)
        routine = WeeklyFitnessRoutineDB(
            routine_id=payload["routine_id"],
            user_id=user_id,
            routine_name=payload["routine_name"],
            plan_snapshot=payload["plan_snapshot"],
            schedule=payload["schedule"],
            status=payload["status"],
        )
        db.add(routine)

        # 2️⃣ Store derived timeline blocks
        for day, day_data in payload["schedule"].items():
            for time_range, block in day_data["timeline"].items():
                db.add(
                    FitnessTimelineBlockDB(
                        id=str(uuid.uuid4()),
                        routine_id=payload["routine_id"],
                        day=day,
                        time_range=time_range,
                        block_type=block["block_type"],
                        category=block["category"],
                        details=block.get("details"),
                    )
                )

        return {
            "data": {
                "routine_id": payload["routine_id"],
                "status": "stored"
            }
        }
