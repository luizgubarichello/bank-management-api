from pydantic import BaseModel, Field
from enum import Enum


class SupportedPaymentMethods(str, Enum):
    """Enum for supported payment methods."""

    DEBIT = "D"
    CREDIT = "C"
    PIX = "P"

    @staticmethod
    def get_taxes() -> dict[type["SupportedPaymentMethods"], float]:
        """Get the taxes for each payment method."""
        return {
            SupportedPaymentMethods.DEBIT: 0.03,
            SupportedPaymentMethods.CREDIT: 0.05,
            SupportedPaymentMethods.PIX: 0.0,
        }


class PaymentMethod(BaseModel):
    """Payment method model."""

    label: SupportedPaymentMethods = Field(...)

    @property
    def tax(self) -> float:
        """Get the tax for the payment method."""
        return SupportedPaymentMethods.get_taxes()[self.label]
