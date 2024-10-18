# Bank Management API

This is a banking management API that allows the creation of accounts and processing of financial transactions through various methods like debit, credit, and Pix. The API is built using Flask, MongoDB, and Pydantic for validation, and follows the MVC pattern.

## Features

- Create accounts with initial balances.
- Retrieve account details.
- Process transactions (debit, credit, Pix) with associated transaction fees.
- Ensure account balances don't go negative.
- Input validation with Pydantic.
- API versioning implemented using `/api/v1`.

---

## Requirements

- Python 3.10 or above
- MongoDB (local instance or MongoDB Atlas)
- `pipenv` or `virtualenv` for environment management (optional but recommended)

---

## Project Structure

```plaintext
bank-management-api/
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── account_controller/
│   │   │   └── __init__.py
│   │   ├── transaction_controller/
│   │   │   ├── __init__.py
│   │   │   └── constants.py
│   ├── models/
│   │   ├── account.py
│   │   ├── payment_method.py
│   │   └── schemas.py
│   └── views/
│       ├── account_routes.py
│       └── transaction_routes.py
├── tests/
|   ├── __init__.py
│   ├── test_accounts.py
│   ├── test_transactions.py
│   └── conftest.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

### 2. Set up a Python Virtual Environment

You can use `virtualenv` or `pipenv` to manage dependencies within a virtual environment:

```bash
# Using virtualenv
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Project Dependencies

Run the following command to install all required Python libraries:

```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB

Ensure MongoDB is running on your local machine or configure a connection to MongoDB Atlas. By default, the API expects MongoDB to be running on `mongodb://localhost:27017/bank_db`.

To run MongoDB locally:

- For **Linux/macOS**, run MongoDB in the background:

  ```bash
  mongod --dbpath /path/to/your/db
  ```

- For **Windows**, you can start MongoDB as a service using the installed service manager or by using the MongoDB shell:

  ```bash
  mongod --dbpath "C:\path\to\your\db"
  ```

You can also use Docker to run MongoDB:

```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

### 5. Set Up the Configuration File

The project uses a `Config` class to define the MongoDB connection settings. You can edit the `config.py` file as needed for custom database URIs or environments.

For example, in `config.py`:

```python
class Config:
    MONGO_URI = "mongodb://localhost:27017/bank_db"  # Edit as needed
```

### 6. Running the Application

Once everything is set up, you can run the Flask app:

```bash
python run.py
```

The API will be accessible at `http://localhost:5000`.

---

## Usage

### Create a New Account

```bash
POST /api/v1/conta
```

**Example Request:**

```json
{
  "numero_conta": 12345,
  "saldo": 100.0
}
```

**Example Response:**

```json
{
  "numero_conta": 12345,
  "saldo": 100.0
}
```

### Get Account Details

```bash
GET /api/v1/conta?numero_conta=<account_number>
```

**Example Response:**

```json
{
  "numero_conta": 12345,
  "saldo": 100.0
}
```

### Process a Transaction

```bash
POST /api/v1/transacao
```

**Example Request (Debit):**

```json
{
  "numero_conta": 12345,
  "valor": 10,
  "forma_pagamento": "D"
}
```

**Example Response:**

```json
{
  "numero_conta": 12345,
  "saldo": 89.7  # after 3% tax
}
```

---

## Running the Tests

The project uses `pytest` for unit testing. To ensure MongoDB is running for the tests, it's recommended to use a separate test database, as defined in `tests/conftest.py`.

### 1. Run the Tests

Use the following command to run the tests:

```bash
pytest
```

This will run all the test cases located in the `tests/` directory. Ensure that the MongoDB instance is running, as the tests rely on MongoDB for account and transaction data.

Tests will automatically clean up any created accounts or transactions after each test case.

---

## API Documentation

### Endpoints

| Method | Endpoint                  | Description                    |
|--------|---------------------------|--------------------------------|
| POST   | `/api/v1/conta`            | Create a new account           |
| GET    | `/api/v1/conta`            | Get account details by number  |
| POST   | `/api/v1/transacao`        | Process a transaction          |

### Request Formats

- **Create Account:** `{ "numero_conta": <int>, "saldo": <float> }`
- **Process Transaction:** `{ "numero_conta": <int>, "valor": <float>, "forma_pagamento": "D" | "C" | "P" }`

### Response Status Codes

- `201`: Created
- `200`: OK
- `400`: Bad Request (validation errors)
- `404`: Not Found (account not found)

---

## Development

- Follow best practices for code formatting and structure.
- All the routes are versioned with `/api/v1` to support future enhancements.
