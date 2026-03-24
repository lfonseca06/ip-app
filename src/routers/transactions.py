from sqlmodel import select
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Query, status

from db import SessionDep
from models import Customer, Transaction, TransactionCreate


router = APIRouter()

#@router.post("/transactions", status_code=status.HTTP_201_CREATED, tags=["transactions"])
@router.post("/transactions", tags=["transactions"])
async def create_transaction(transaction_data:TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    return transaction_data


@router.get("/transactions", tags=["transactions"])
async def list_transaction(
    session: SessionDep, 
    skip: int = Query(0, description="Registros a omitir"),
    limit:int=Query(5, description="Número de resgistro")
):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions