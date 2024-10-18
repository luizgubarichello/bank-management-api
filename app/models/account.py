from bson import ObjectId
from pydantic import BaseModel, Field


class Account(BaseModel):
    """Account model."""

    id: ObjectId | None = Field(default_factory=ObjectId, alias="_id")
    numero_conta: int = Field(..., ge=0)
    saldo: float = Field(..., ge=0)

    def get_metadata(self) -> dict:
        """Get the account as a JSON object.

        Returns:
            dict: The account as a JSON object.
        """
        return self.model_dump(by_alias=True, exclude={"id"})

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
