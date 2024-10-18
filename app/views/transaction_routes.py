from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from pydantic import ValidationError

from app.controllers.transaction_controller import process_transaction
from app.models.schemas import TransactionSchema
from app.models.payment_method import PaymentMethod

transaction_bp = Blueprint("transaction_bp", __name__)


@transaction_bp.route("", methods=["POST"])
def handle_transaction() -> tuple[Response, int]:
    """Handle a transaction.

    Returns:
        tuple[Response, int]: A tuple containing the response and the status code.
    """
    try:
        data = TransactionSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except TypeError as e:
        return jsonify({"message": "Invalid data"}), 400
    try:
        new_balance = process_transaction(
            data.numero_conta,
            data.valor,
            PaymentMethod(label=data.forma_pagamento),
        )
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"numero_conta": data.numero_conta, "saldo": new_balance}), 201
