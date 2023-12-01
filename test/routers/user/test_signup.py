def test_example(test_client):
    response = test_client.post(
        "/api/user/signup",
        json={"email": "test@test.com", "password": "123456", "username": "test"},
    )
    assert response.status_code == 201
