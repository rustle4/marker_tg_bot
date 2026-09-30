from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tg_auth import TelegramInitData
from app.users.model import User


async def create_get_user(db: AsyncSession, data: TelegramInitData) -> User:
    result = await db.execute(select(User).where(User.telegram_id == data.telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegramid=data.telegram_id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user


async def get_user_by_tg_id(db: AsyncSession, telegram_id: int) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))

    return result.scalar_one_or_none()
