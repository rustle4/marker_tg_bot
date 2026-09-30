from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.tg_auth import TelegramInitData, get_init_data
from app.users.crud import create_get_user
from app.users.model import User


async def get_current_user(
    init_data: Annotated[TelegramInitData, Depends(get_init_data)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    return await create_get_user(db, init_data)


CurrentUser = Annotated[User, Depends(get_current_user)]
