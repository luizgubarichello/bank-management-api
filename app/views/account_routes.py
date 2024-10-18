from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from pydantic import ValidationError

from app.controllers.account_controller import create_account, get_account
from app.models.schemas import CreateAccountSchema, GetAccountSchema

account_bp = Blueprint("account_bp", __name__)


@account_bp.route("", methods=["POST"])
def create_new_account() -> tuple[Response, int]:
    """Create a new account.

    Returns:
        tuple[Response, int]: A tuple containing the response and the status code.
    """
    try:
        data = CreateAccountSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except TypeError as e:
        return jsonify({"message": "Invalid data"}), 400
    account = create_account(data.numero_conta, data.saldo)
    if not account:
        return jsonify({"message": "Account already exists or invalid data"}), 400
    return jsonify(account.get_metadata()), 201


@account_bp.route("", methods=["GET"])
def get_account_info() -> tuple[Response, int]:
    """Get account information.

    Returns:
        tuple[Response, int]: A tuple containing the response and the status code.
    """
    try:
        data = GetAccountSchema(**request.args)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except TypeError as e:
        return jsonify({"message": "Invalid data"}), 400
    account = get_account(data.numero_conta)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    return jsonify(account.get_metadata()), 200
