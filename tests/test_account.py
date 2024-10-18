import json


def test_create_new_account(test_client):
    response = test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json == {"numero_conta": 12345, "saldo": 100.0}


def test_create_existing_account(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Account already exists" in response.json["message"]


def test_get_existing_account(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.get("/api/v1/conta?numero_conta=12345")
    assert response.status_code == 200
    assert response.json == {"numero_conta": 12345, "saldo": 100.0}


def test_get_non_existing_account(test_client):
    response = test_client.get("/api/v1/conta?numero_conta=99999")
    assert response.status_code == 404
    assert "Account not found" in response.json["message"]


def test_create_account_invalid_balance(test_client):
    response = test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": -10.0}), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Input should be greater than or equal" in response.json["message"][0]["msg"]


def test_create_account_invalid_account_number(test_client):
    response = test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": -1, "saldo": 100.0}), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Input should be greater than or equal" in response.json["message"][0]["msg"]
