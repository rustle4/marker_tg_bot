from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    
    model_config = ConfigDict(from_attributes=True)