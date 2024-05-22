from fastapi import HTTPException, status

DICT_ACCOUNTS = {}


def reset():
    global DICT_ACCOUNTS
    DICT_ACCOUNTS = {}


class Bank:
    def __init__(self, account_id: str):
        self.account_id = account_id

    def get_balance(self) -> dict:
        if not self.account_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={'message': 'Account ID is required'})

        if self.account_id not in DICT_ACCOUNTS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Account ID {self.account_id} does not exist')

        return DICT_ACCOUNTS[self.account_id]['balance']

    def deposit(self, amount: float) -> dict:
        if not self.account_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if self.account_id not in DICT_ACCOUNTS:
            DICT_ACCOUNTS[self.account_id] = {
                'balance': amount,
            }

        else:
            DICT_ACCOUNTS[self.account_id]['balance'] += amount

        response = {
            'destination': {
                'id': self.account_id,
                'balance': DICT_ACCOUNTS[self.account_id]['balance']
            }
        }

        return response

    def withdraw(self, amount: float) -> dict:
        if not self.account_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if self.account_id not in DICT_ACCOUNTS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if amount > DICT_ACCOUNTS[self.account_id]['balance']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        DICT_ACCOUNTS[self.account_id]['balance'] -= amount

        response = {
            'origin': {
                'id': self.account_id,
                'balance': DICT_ACCOUNTS[self.account_id]['balance']
            }
        }

        return response

    def transfer(self, amount: float, destination_id: str) -> dict:
        if not self.account_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if self.account_id not in DICT_ACCOUNTS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if destination_id not in DICT_ACCOUNTS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if amount > DICT_ACCOUNTS[self.account_id]['balance']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        DICT_ACCOUNTS[self.account_id]['balance'] -= amount
        DICT_ACCOUNTS[destination_id]['balance'] += amount

        response = {
            'origin': {
                'id': self.account_id,
                'balance': DICT_ACCOUNTS[self.account_id]['balance']
            },
            'destination': {
                'id': destination_id,
                'balance': DICT_ACCOUNTS[destination_id]['balance']
            }
        }
        
        return response
