from app.controllers.account_controller import get_account, update_account_balance
from app.controllers.transaction_controller.constants import Constants
from app.models.payment_method import PaymentMethod


def process_transaction(account_number: int, value: float, payment_method: PaymentMethod) -> float:
    """Process a transaction.

    Args:
        account_number (int): Account number.
        value (float): Transaction value.
        payment_method (PaymentMethod): Payment method.

    Returns:
        float: The new balance.

    Raises:
        ValueError: If the account does not exist, the payment method is invalid, or the account has insufficient funds.
    """
    account = get_account(account_number)
    if not account:
        raise ValueError(Constants.ErrorMessages.ACCOUNT_NOT_FOUND)
    post_tax_value = value * (1 + payment_method.tax)
    if account.saldo < post_tax_value:
        raise ValueError(Constants.ErrorMessages.INSUFFICIENT_FUNDS)
    new_balance = account.saldo - post_tax_value
    update_account_balance(account, new_balance)
    return new_balance
