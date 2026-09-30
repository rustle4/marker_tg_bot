from api.notes import router as notes_router
from fastapi import APIRouter

from app.api.goals import router as goals_router
from app.api.habits import router as habits_router
from app.api.pomodoro import router as pomodoro_router

api_router = APIRouter(prefix="/api")

api_router.include_router(goals_router)
api_router.include_router(notes_router)
api_router.include_router(habits_router)
api_router.include_router(pomodoro_router)
