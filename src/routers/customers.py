from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan, StatusEnum, Transaction
from db import SessionDep

from fastapi import APIRouter, status, HTTPException, FastAPI, Query
from sqlmodel import select


router = APIRouter()

#LEER
@router.post(
    "/customers", 
    response_model=Customer, 
    status_code=status.HTTP_201_CREATED,
    tags=['customers'],
)
async def create_customer(customer_data:CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

#LEER
@router.get("/customers/{customer_id}", response_model=Customer, tags=['customers'])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

#ACTUALIZAR
@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['customers'])
async def read_customer(customer_id: int, customer_data:CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")    
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

#ELIMINAR
@router.delete("/customers/{customer_id}", tags=['customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
            )
    session.delete(customer_db)
    session.commit()
    return {"detail":"Ok"}

#LISTAR
@router.get("/customers", response_model=list[Customer], tags=['customers'])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.post("/customers/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = customer = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente o el plan no existen")
    
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.post("/customers/{customer_id}/plans")
async def subscribe_customer_to_plan(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    query = (select(CustomerPlan).where(CustomerPlan.customer_id==customer_id).where(CustomerPlan.status==plan_status))
    plans = session.exec(query).all()
    return plans