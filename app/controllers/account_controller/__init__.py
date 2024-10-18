from pydantic import ValidationError

from app import mongo
from app.models.account import Account


def create_account(account_number: int, balance: float) -> Account | None:
    """Create a new account.

    Args:
        account_number (int): Account number.
        balance (float): Account balance.

    Returns:
        Account | None: The created account or None in case of an error.
    """
    if mongo.db.accounts.find_one({"numero_conta": account_number}):
        return None
    try:
        account = Account(numero_conta=account_number, saldo=balance)
    except ValidationError:
        return None
    account.id = mongo.db.accounts.insert_one({"numero_conta": account_number, "saldo": balance}).inserted_id
    return account


def get_account(account_number: int) -> Account | None:
    """Get an account by its account number.

    Args:
        account_number (int): Account number.

    Returns:
        Account | None: The account or None if the account does not exist.
    """
    account = mongo.db.accounts.find_one({"numero_conta": account_number})
    if not account:
        return None
    return Account(numero_conta=account["numero_conta"], saldo=account["saldo"], _id=account["_id"])


def update_account_balance(account: Account, new_balance: float) -> None:
    """Update an account balance.

    Args:
        account (Account): Account to update.
        new_balance (float): New account balance.
    """
    mongo.db.accounts.update_one({"_id": account.id}, {"$set": {"saldo": new_balance}})
