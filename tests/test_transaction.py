import json


def test_process_valid_debit_transaction(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/transacao",
        data=json.dumps({"numero_conta": 12345, "valor": 10, "forma_pagamento": "D"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"numero_conta": 12345, "saldo": 89.7}


def test_process_valid_credit_transaction(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/transacao",
        data=json.dumps({"numero_conta": 12345, "valor": 10, "forma_pagamento": "C"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"numero_conta": 12345, "saldo": 89.5}


def test_process_pix_transaction(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/transacao",
        data=json.dumps({"numero_conta": 12345, "valor": 10, "forma_pagamento": "P"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {"numero_conta": 12345, "saldo": 90.0}


def test_insufficient_funds_debit_transaction(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 5.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/transacao",
        data=json.dumps({"numero_conta": 12345, "valor": 10, "forma_pagamento": "D"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "Insufficient funds." in response.json["message"]


def test_invalid_payment_method(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/transacao",
        data=json.dumps({"numero_conta": 12345, "valor": 10, "forma_pagamento": "X"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    print(response.json)
    assert "Input should be" in response.json["message"][0]["msg"]


def test_transaction_invalid_amount(test_client):
    test_client.post(
        "/api/v1/conta", data=json.dumps({"numero_conta": 12345, "saldo": 100.0}), content_type="application/json"
    )

    response = test_client.post(
        "/api/v1/transacao",
        data=json.dumps({"numero_conta": 12345, "valor": -10, "forma_pagamento": "D"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "Input should be greater than or equal to" in response.json["message"][0]["msg"]
