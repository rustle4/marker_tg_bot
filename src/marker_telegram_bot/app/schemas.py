from pydantic import BaseModel

from src.marker_telegram_bot.app.models import Note


class GoalCreate(BaseModel):
    telegram_id: int
    title: int


class NoteCreate(BaseModel):
    telegram_id: int
    title: str | None = None
    desciption: str
    note_type: Note.NoteType = Note.NoteType.FAST

class HabitCreate(BaseModel):
    telegram_id: int
    title: str

class PomodoroStart(BaseModel):
    telegram_id: int
    duration_minutes: int = 25