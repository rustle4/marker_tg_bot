from pydantic import BaseModel, ConfigDict


class GoalCreate(BaseModel):
    title: str


class GoalUpdate(BaseModel):
    title: str | None = None
    is_achieved: bool | None = None


class GoalResponse(BaseModel):
    id: int
    title: str
    is_achieved: bool

    model_config = ConfigDict(from_attributes=True)
