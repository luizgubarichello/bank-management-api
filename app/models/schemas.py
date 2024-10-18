from pydantic import BaseModel, Field

from app.models.payment_method import SupportedPaymentMethods


class CreateAccountSchema(BaseModel):
    """CreateAccountSchema model."""

    numero_conta: int = Field(..., ge=0)
    saldo: float = Field(..., ge=0)


class GetAccountSchema(BaseModel):
    """GetAccountSchema model."""

    numero_conta: int = Field(..., ge=0)


class TransactionSchema(BaseModel):
    """TransactionSchema model."""

    numero_conta: int = Field(..., ge=0)
    valor: float = Field(..., ge=0)
    forma_pagamento: SupportedPaymentMethods = Field(...)
