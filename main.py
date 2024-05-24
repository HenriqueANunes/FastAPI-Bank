from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.custom_http_exception import CustomHttpException

import services.account


class Transaction(BaseModel):
    type: str
    amount: float
    destination: str | None = None
    origin: str | None = None


app = FastAPI()


@app.exception_handler(CustomHttpException)
async def custom_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )


@app.post("/reset")
async def reset():
    return services.account.reset()


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
        raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST, content=0)

    return response
