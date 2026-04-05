# backend/app/models/__init__.py
from .user import User
from .refresh_token import RefreshToken
from .goal import Goal
from .task import Task
from .subtask import Subtask
from .activity import Activity
from .habit import Habit
from .notification import Notification
from app.models.routine_event import RoutineEvent
from app.models.reminder import Reminder   # 🔥 THIS LINE IS REQUIRED
from app.models.google_token import GoogleToken