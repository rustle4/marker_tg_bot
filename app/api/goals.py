from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Goal
from app.schemas import GoalCreate

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/{telegram_id}")
async def get_goals(telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Goal)
        .where(Goal.telegram_id == telegram_id)
        .order_by(Goal.created_at.desc())
    )
    return result.scalars().all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_goal(data: GoalCreate, db: AsyncSession = Depends(get_db)):
    goal = Goal(user_id=data.telegram_id, title=data.title)
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.patch("/{goal_id}/toggle")
async def toggle_goal(goal_id: int, db: AsyncSession = Depends(get_db)):
    goal = await db.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    goal.is_completed = not goal.is_completed
    await db.commit()
    return goal


@router.delete("/{goal_id}")
async def delete_goal(goal_id: int, db: AsyncSession = Depends(get_db)):
    goal = await db.get(Goal, goal_id)
    if goal:
        await db.delete(goal)
        await db.commit()
    return {"success": True}
