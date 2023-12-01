SIGNUP_URL = "/api/user/signup"


def test_signup_success(test_client):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "password": "123456", "username": "test"},
    )
    assert response.status_code == 201


def test_signup_invalid_email(test_client):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": "test", "password": "123456", "username": "test"},
    )
    assert response.status_code == 400


def test_signup_missing_details(test_client):
    response_missing_email = test_client.post(
        SIGNUP_URL,
        json={"password": "123456", "username": "test"},
    )
    assert response_missing_email.status_code == 400

    response_missing_password = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "username": "test"},
    )
    assert response_missing_password.status_code == 400


def test_signup_duplicate_emails(test_client):
    # First signup
    response_first_signup = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "password": "123456", "username": "test"},
    )
    assert response_first_signup.status_code == 201

    # Second signup with the same email
    response_second_signup = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "password": "123456", "username": "test"},
    )
    assert response_second_signup.status_code == 400


def test_signup_sets_cookie(test_client):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "password": "123456", "username": "test"},
    )
    assert response.status_code == 201
    assert "Set-Cookie" in response.headers
