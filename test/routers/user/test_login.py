from sqlalchemy import text
import pytest
from test.conftest import TestingSessionLocal

LOGIN_URL = "/api/user/login"
TEST_USER_EMAIL = "test@test.com"


def test_login_success(test_client, seed_database_user):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": TEST_USER_EMAIL,
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


def test_login_invalid_password(test_client):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": TEST_USER_EMAIL,
            "password": "1234567",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": [{"message": "Incorrect email or password", "code": None}]
    }


def test_login_invalid_username(test_client):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": "test@bla.com",
            "password": "password",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": [{"message": "Incorrect email or password", "code": None}]
    }


def test_missing_details(test_client):
    response_missing_email = test_client.post(
        LOGIN_URL,
        data={"password": "password"},
    )
    assert response_missing_email.status_code == 422
    assert response_missing_email.json() == {
        "detail": [
            {
                "code": "value_error.missing",
                "message": "field required",
                "code": "value_error.missing",
            }
        ]
    }
    response_missing_password = test_client.post(
        LOGIN_URL,
        data={"username": TEST_USER_EMAIL},
    )
    assert response_missing_password.status_code == 422
    assert response_missing_password.json() == {
        "detail": [
            {
                "code": "value_error.missing",
                "message": "field required",
                "code": "value_error.missing",
            }
        ]
    }


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
