from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep

router = APIRouter()

#LEER
@router.post("/customers", response_model=Customer)
async def create_customer(customer_data:CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

#LEER
@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")    
    return customer_db


#ACTUALIZAR
@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
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
@router.delete("/customers/{customer_id}")
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
@router.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()