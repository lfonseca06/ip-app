from fastapi import APIRouter

from models import Plan
from db import SessionDep

router = APIRouter()

@router.post("/plans")
def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add()
    session.commit()
    session.reresh(plan_db)
    return
    