# backend/app/main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth_routes, user_routes,activity_routes,goal_routes,criteria_routes,task_routes,subtask_routes,analytics_routes,proposal_routes, agent_routes,chat_routes  # ensure package importable via __init__.py
from app.models import user as user_model  # to ensure models are registered
from app.models import refresh_token as refresh_model
from app.crud import goal_crud

# import other models so Base.metadata.create_all knows about them
from app.models.task import Task
from app.models.goal import Goal
from app.models.subtask import Subtask
from app.models.activity import Activity
from app.models.habit import Habit
from app.models.notification import Notification
from app.models.summary import Summary
from my_agent.models.action_proposal import ActionProposal
from my_agent.models.agent_run import AgentRun
from my_agent.models.approval_decision import ApprovalDecision
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.auth import AuthMiddleware
# Create tables (for dev). Use Alembic for production migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Routine Planner Auth")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware, protected = [
  "/users","/goals","/activities","/tasks","/subtasks",
  "/analytics","/proposals"
])

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(criteria_routes.router, prefix='/criteria')
app.include_router(activity_routes.router, prefix="/activities")
app.include_router(goal_routes.router, prefix="/goals")
app.include_router(task_routes.router, prefix="/tasks")
app.include_router(subtask_routes.router, prefix="/subtasks")
app.include_router(analytics_routes.router, prefix="/analytics")
app.include_router(proposal_routes.router, prefix="/proposals")
app.include_router(agent_routes.router, prefix="/agent")
app.include_router(chat_routes.router, prefix="/chat")
  
