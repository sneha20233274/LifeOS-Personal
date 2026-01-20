# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.routes import (
    auth_routes,
    user_routes,
    activity_routes,
    goal_routes,
    criteria_routes,
    task_routes,
    subtask_routes,
    analytics_routes,
    proposal_routes,
    agent_routes,
    chat_routes,
    routine_event_routes,
    reminder_routes,
    google_auth,
    fitness
)

# Ensure models are registered
from app.models.user import User
from app.models.goal import Goal
from app.models.task import Task
from app.models.subtask import Subtask
from app.models.activity import Activity
from app.models.habit import Habit
from app.models.notification import Notification
from app.models.summary import Summary
from my_agent.models.action_proposal import ActionProposal
from my_agent.models.agent_run import AgentRun
from my_agent.models.approval_decision import ApprovalDecision
from app.models.routine_event import RoutineEvent
from app.models.reminder import Reminder

from app.core.scheduler import start_scheduler
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Routine Planner")
@app.on_event("startup")
def startup_event():
    start_scheduler()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 🔒 ONE origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(criteria_routes.router, prefix="/criteria")
app.include_router(activity_routes.router, prefix="/activities")
app.include_router(goal_routes.router, prefix="/goals")
app.include_router(task_routes.router, prefix="/tasks")
app.include_router(subtask_routes.router, prefix="/subtasks")
app.include_router(analytics_routes.router, prefix="/analytics")
app.include_router(proposal_routes.router, prefix="/proposals")
app.include_router(agent_routes.router, prefix="/agent")
app.include_router(chat_routes.router, prefix="/chat")
app.include_router(routine_event_routes.router , prefix='/routine-events')
app.include_router(reminder_routes.router)
app.include_router(fitness.router,prefix="/fitness")
app.include_router(google_auth.router , prefix='/integrations/google')
