from fastapi import HTTPException, status

DICT_ACCOUNTS = {}


def reset():
    global DICT_ACCOUNTS
    DICT_ACCOUNTS = {}


class Bank:
    def __init__(self, account_id: str):
        self.account_id = account_id

    def get_balance(self):
        if not self.account_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={'message': 'Account ID is required'})

        if self.account_id not in DICT_ACCOUNTS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Account ID {self.account_id} does not exist')

        return DICT_ACCOUNTS[self.account_id]['balance']

    def deposit(self, amount: float):
        if not self.account_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if self.account_id not in DICT_ACCOUNTS:
            DICT_ACCOUNTS[self.account_id] = {
                'amount': amount,
            }

        else:
            DICT_ACCOUNTS[self.account_id]['amount'] += amount

        return {'destination': {'id': self.account_id, 'amount': amount}}
