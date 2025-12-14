# backend/app/main.py
from fastapi import FastAPI
from core.database import engine, Base
from routes import auth_routes, user_routes,activity_routes,goal_routes,criteria_routes  # ensure package importable via __init__.py
from models import user as user_model  # to ensure models are registered
from models import refresh_token as refresh_model

# import other models so Base.metadata.create_all knows about them
from models.task import Task
from models.goal import Goal
from models.subtask import Subtask
from models.activity import Activity
from models.habit import Habit
from models.notification import Notification


from middleware.auth import AuthMiddleware
# Create tables (for dev). Use Alembic for production migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Routine Planner Auth")

app.add_middleware(AuthMiddleware, protected = [
  "/users","/goals","/activities"
])

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(criteria_routes.router, prefix='/criteria')
app.include_router(activity_routes.router, prefix="/activities")
app.include_router(goal_routes.router, prefix="/goals")
