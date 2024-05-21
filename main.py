from fastapi import FastAPI, status
import services.bank

app = FastAPI()


@app.get("/reset")
async def reset():
    services.bank.reset()
    return 'OK'


@app.get("/balance", status_code=status.HTTP_200_OK)
async def balance(account_id: str):
    return services.bank.Bank(account_id=account_id).get_balance()


@app.post("/event", status_code=status.HTTP_201_CREATED)
async def event(type: str, destination: str, amount: float):

    if type == 'deposit':
        return services.bank.Bank(account_id=destination).deposit(amount=amount)
