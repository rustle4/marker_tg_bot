from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from sqlalchemy import select, update

from src.marker_telegram_bot.app.models import Goal, User
from src.marker_telegram_bot.core.database import AsyncSessionLocal

router = Router()


@router.message(Command("goal"))
async def set_goal(message: Message) -> None:
    cmd_args = message.text.split(maxsplit=1)
    if len(cmd_args) < 2:
        await message.answer(
            "Something went wrong!\n"
            "Please, try again. Example of setting a goal: /goal [name of your goal]\n"
            "You got this!"
        )
        return

    goal_name = cmd_args[1]
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:
        statement = select(User).where(User.telegram_id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=user_id, username=message.from_user.username)
            session.add(user)

        new_goal = Goal(telegram_id=user_id, title=goal_name)
        session.add(new_goal)
        await session.commit()

    await message.answer(f"Goal '{goal_name}' was added succesfully!")


@router.message(Command("goals"))
async def show_goals(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        statement = select(Goal).where(
            Goal.telegram_id == message.from_user.id, Goal.is_achieved == False
        )
        result = await session.execute(statement)
        goals = result.scalars().all()

    if not goals:
        await message.answer("You have no goals for now.")
        return

    for goal in goals:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Did it!", callback_data=f"complete_{goal.id}"
                    )
                ]
            ]
        )
        await message.answer(f"{goal.title}", reply_markup=keyboard)


@router.callback_query(F.data.startswith("complete_"))
async def goal_achieved_callback(callback: CallbackQuery) -> None:
    goal_id = int(callback.data.split("_")[1])

    async with AsyncSessionLocal() as session:
        statement = update(Goal).where(Goal.id == goal_id).values(is_achieved=True)
        await session.execute(statement)
        await session.commit()

    await callback.answer("Goal achieved!")
    await callback.message.edit_text(f"{callback.message.text}\n\nAchieved!")
