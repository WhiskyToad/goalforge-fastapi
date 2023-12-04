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
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "message": "value is not a valid email address",
                "code": "value_error.email",
            }
        ]
    }


def test_signup_missing_details(test_client):
    response_missing_email = test_client.post(
        SIGNUP_URL,
        json={"password": "123456", "username": "test"},
    )
    assert response_missing_email.status_code == 422
    print(response_missing_email.json())
    assert response_missing_email.json() == {
        "detail": [{"message": "field required", "code": "value_error.missing"}]
    }

    response_missing_password = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "username": "test"},
    )
    assert response_missing_password.status_code == 422
    assert response_missing_password.json() == {
        "detail": [{"message": "field required", "code": "value_error.missing"}]
    }


def test_signup_duplicate_emails(test_client):
    # Second signup with the same email
    response_second_signup = test_client.post(
        SIGNUP_URL,
        json={"email": "test@test.com", "password": "123456", "username": "test"},
    )
    assert response_second_signup.status_code == 400
    assert response_second_signup.json() == {
        "detail": [{"message": "Email already exists", "code": "email"}]
    }


def test_signup_sets_cookie(test_client):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": "test1@test.com", "password": "123456", "username": "test"},
    )
    assert response.status_code == 201
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"
