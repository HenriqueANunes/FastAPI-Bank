from fastapi import status

from services.custom_http_exception import CustomHttpException

DICT_ACCOUNTS = {}


def reset():
    global DICT_ACCOUNTS
    DICT_ACCOUNTS = {}
    return 'OK'


class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id

    def get_balance(self) -> dict:
        if not self.account_id:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Account ID is required'})

        if self.account_id not in DICT_ACCOUNTS:
            raise CustomHttpException(status_code=status.HTTP_404_NOT_FOUND,
                                      content='0')

        return DICT_ACCOUNTS[self.account_id]['balance']

    def deposit(self, amount: float) -> dict:
        if not self.account_id:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Account ID is required'})

        if amount < 0:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Amount must be greater than 0'})

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
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Account ID is required'})

        if amount < 0:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Amount must be greater than 0'})

        if self.account_id not in DICT_ACCOUNTS:
            raise CustomHttpException(status_code=status.HTTP_404_NOT_FOUND,
                                      content='0')

        if amount > DICT_ACCOUNTS[self.account_id]['balance']:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Insufficient funds'})

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
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Account ID is required'})

        if amount < 0:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Amount must be greater than 0'})

        if self.account_id not in DICT_ACCOUNTS:
            raise CustomHttpException(status_code=status.HTTP_404_NOT_FOUND,
                                      content='0')

        if destination_id not in DICT_ACCOUNTS:
            raise CustomHttpException(status_code=status.HTTP_404_NOT_FOUND,
                                      content='0')

        if amount > DICT_ACCOUNTS[self.account_id]['balance']:
            raise CustomHttpException(status_code=status.HTTP_400_BAD_REQUEST,
                                      content={'message': 'Insufficient funds'})

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
