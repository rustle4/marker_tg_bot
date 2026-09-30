from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.goals.model import Goal
from app.goals.schemas import GoalCreate, GoalUpdate


async def create_goal(db: AsyncSession, telegram_id: int, data: GoalCreate) -> Goal:
    goal = Goal(telegram_id=telegram_id, **data.model_dump())
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


async def update_goal(
    db: AsyncSession, telegram_id: int, goal_id: int, data: GoalUpdate
) -> Goal | None:
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.telegram_id == telegram_id)
    )
    updated_goal = result.scalar_one_or_none()
    if updated_goal is None:
        return None

    values = data.model_dump(exclude_unset=True)
    if "is_done" in values:
        updated_goal.is_achieved = values.pop("is_done")

    for field, value in values.items():
        setattr(updated_goal, field, value)

    await db.commit()
    await db.refresh(updated_goal)
    return updated_goal


async def list_goals(db: AsyncSession, telegram_id: int) -> list[Goal]:
    result = await db.execute(
        select(Goal)
        .where(Goal.telegram_id == telegram_id)
        .order_by(Goal.is_achieved.asc())
    )
    return list(result.scalars())
