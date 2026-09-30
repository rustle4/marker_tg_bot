from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import CurrentUser
from app.core.database import get_db
from app.goals import crud as goal_crud
from app.goals.schemas import GoalCreate, GoalResponse, GoalUpdate
from app.users.schemas import UserResponse

router = APIRouter(prefix="/api")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    payload: GoalCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await goal_crud.create_goal(db, current_user.id, payload)


@router.get("/goals", response_model=list[GoalResponse])
async def list_goals(
    current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await goal_crud.list_goals(db, current_user.id)


@router.get("/goals/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    payload: GoalUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    goal = await goal_crud.update_goal(db, current_user.id, goal_id, payload)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    return goal
