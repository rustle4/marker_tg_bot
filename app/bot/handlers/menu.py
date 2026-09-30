from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import User

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    tg_user = message.from_user

    async with AsyncSessionLocal() as session:
        statement = select(User).where(User.telegram_id == tg_user.id)
        result = await session.execute(statement)
        db_user = result.scalar_one_or_none()

        if not db_user:
            db_user = User(telegram_id=tg_user.id, username=tg_user.username)
            session.add(db_user)
            await session.commit()

    await message.answer(
        "Hello, this is Marker bot.\n"
        "What can I do for you?\n"
        "Actually, right now I can't do anything:(\n"
        "BUT I have this for you<3\n"
    )

    gif_url_love = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXFvZWNod2FubDNmNWFoNWoxYzhqNWRzbnltOXBoemVtMjZzMGZudyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nM2ARuUlLtB0t3OKHm/giphy.gif"

    await message.answer_animation(animation=gif_url_love, caption="We love you!")
