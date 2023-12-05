LOGIN_URL = "/api/user/login"


def test_login_success(test_client):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": "test@test.com",
            "password": "123456",
        },
    )
    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


def test_login_invalid_password(test_client):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": "test@test.com",
            "password": "1234567",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_invalid_username(test_client):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": "test@bla.com",
            "password": "123456",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_missing_details(test_client):
    response_missing_email = test_client.post(
        LOGIN_URL,
        data={"password": "123456"},
    )
    assert response_missing_email.status_code == 422
    assert response_missing_email.json() == {
        "detail": [{"message": "field required", "code": "value_error.missing"}]
    }
    response_missing_password = test_client.post(
        LOGIN_URL,
        data={"email": "test@test.com"},
    )
    assert response_missing_password.status_code == 422
    assert response_missing_password.json() == {
        "detail": [{"message": "field required", "code": "value_error.missing"}]
    }
