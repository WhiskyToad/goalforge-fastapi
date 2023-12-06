from sqlalchemy import text
import pytest
from test.conftest import TestingSessionLocal

ME_ROUTE = "/api/user/me"


def test_read_users_me_with_valid_token(test_client, seed_database_user):
    # Provide a valid token for testing
    valid_token = seed_database_user

    response = test_client.get(
        ME_ROUTE,
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    assert response.json().get("email") == "test@test.com"
    assert response.json().get("username") == "test_user"


def test_read_users_me_with_invalid_token(test_client):
    # Provide an invalid token for testing
    invalid_token = "bleh"

    response = test_client.get(
        ME_ROUTE,
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": [{"message": "JWT Error", "code": None}]}


# Create a fixture for cleaning up the mock database after tests
@pytest.fixture(scope="module", autouse=True)
def cleanup_database():
    # This fixture will be executed after all tests in the module
    # Clean up the mock database, delete all test data, etc.
    db = TestingSessionLocal()
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()
    yield
    # Any cleanup code to run after all tests
    pass
