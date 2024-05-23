from fastapi import FastAPI, status
from pydantic import BaseModel

import services.account


class Transaction(BaseModel):
    type: str
    amount: float
    destination: str | None = None
    origin: str | None = None


app = FastAPI()


@app.post("/reset")
async def reset():
    services.account.reset()
    return 'OK'


@app.get("/balance", status_code=status.HTTP_200_OK)
async def balance(account_id: str):
    return services.account.Account(account_id=account_id).get_balance()


@app.post("/event", status_code=status.HTTP_201_CREATED)
async def event(transaction: Transaction):

    if transaction.type == 'deposit':
        response = services.account.Account(account_id=transaction.destination).deposit(amount=transaction.amount)

    elif transaction.type == 'withdraw':
        response = services.account.Account(account_id=transaction.origin).withdraw(amount=transaction.amount)

    elif transaction.type == 'transfer':
        response = services.account.Account(account_id=transaction.origin).transfer(amount=transaction.amount,
                                                                                 destination_id=transaction.destination)
    else:
        raise status.HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return response
