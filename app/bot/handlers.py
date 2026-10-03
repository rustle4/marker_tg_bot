from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import goal_keyboard
from app.core.tg_auth import TelegramInitData
from app.goals import crud as goal_crud
from app.goals.schemas import GoalCreate
from app.users.crud import create_get_user

router = Router()


def telegram_data(message: Message) -> TelegramInitData:
    user = message.from_user
    assert user is not None
    return TelegramInitData(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@router.message(CommandStart())
async def start(message: Message, db: AsyncSession):
    user = await create_get_user(db, telegram_data(message))
    name = user.first_name or user.username or "user"

    await message.answer(
        f"Hello {name}, this is Marker bot.\n\n"
        "What can i do for you:\n"
        "* /goal [goal name] - add your goal\n"
        "* /goals - list of your goals\n"
    )


@router.message(Command("goal"))
async def create_goal(message: Message, cmd: CommandObject, db: AsyncSession):
    title = (cmd.args or "").strip()
    if not title:
        await message.answer("Example: /goal [your goal]")
        return
    user = await create_get_user(db, telegram_data(message))
    goal = await goal_crud.create_goal(db, user.id, GoalCreate(title=title))
    await message.answer(
        f"Goal added: {goal.title}", reply_markup=goal_keyboard(goal.id)
    )


@router.message(Command("goals"))
async def list_goals(message: Message, db: AsyncSession):
    user = await create_get_user(db, telegram_data(message))
    goals = await goal_crud.list_goals(db, user.id)
    if not goals:
        await message.answer("There are no goals yet.")
        return
    for goal in goals:
        status = "done" if goal.is_achieved else "not done"
        keyboard = None if goal.is_achieved else goal_keyboard(goal.id)
        await message.answer(f"{status} {goal.title}", reply_markup=keyboard)
