import pytest

from app import create_app, mongo


class Config:
    """Application configuration."""

    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/test_bank_db"


@pytest.fixture(scope="module")
def test_client():
    """Create a Flask test client instance."""
    app = create_app(Config)

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="function", autouse=True)
def clean_mongo():
    """Clean the MongoDB database."""
    mongo.db.accounts.delete_many({})
