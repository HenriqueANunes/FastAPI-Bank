from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.custom_http_exception import CustomHttpException

import services.account


class Transaction(BaseModel):
    """
    A class to represent a transaction.

    Attributes
    ----------
    type : str
        a string that represents the type of transaction (deposit, withdraw, transfer)
    amount : float
        a float that represents the amount of the transaction
    destination : str | None
        a string that represents the destination account id of the transaction (for deposit and transfer)
    origin : str | None
        a string that represents the origin account id of the transaction (for withdraw and transfer)
    """
    type: str
    amount: float
    destination: str | None = None
    origin: str | None = None


# Initialize FastAPI application
app = FastAPI()


@app.exception_handler(CustomHttpException)
async def custom_exception_handler(request: Request, exc: CustomHttpException):
    """
    Exception handler for CustomHttpException.

    Parameters
    ----------
    request : Request
        the request that caused the exception
    exc : CustomHttpException
        the exception that was raised

    Returns
    -------
    JSONResponse
        a JSON response with the status code and content of the exception
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )


@app.post("/reset")
async def reset():
    """
    Endpoint to reset the bank data.

    Returns
    -------
    str
        a string indicating the result of the reset operation
    """
    return services.account.reset()


@app.get("/balance", status_code=status.HTTP_200_OK)
async def balance(account_id: str):
    """
    Endpoint to get the balance of an account.

    Parameters
    ----------
    account_id : str
        the id of the account

    Returns
    -------
    dict
        a dictionary with the balance of the account
    """
    return services.account.Account(account_id=account_id).get_balance()


@app.post("/event", status_code=status.HTTP_201_CREATED)
async def event(transaction: Transaction):
    """
    Endpoint to perform a transaction.

    Parameters
    ----------
    transaction : Transaction
        the transaction to be performed

    Returns
    -------
    dict
        a dictionary with the result of the transaction

    Raises
    ------
    CustomHttpException
        if the transaction is invalid
    """
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
