from test.conftest import TestingSessionLocal
from app.models.UserModel import UserModel
from app.utils.security import SecurityUtils
from app.services.JwtService import JwtService


def seed_database_user():
    db = TestingSessionLocal()
    # Create a test user in the database
    hashed_password = SecurityUtils().get_password_hash("password")
    user = UserModel(
        email="test@test.com",
        hashed_password=hashed_password,
        username="test_user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    # Generate a token for the test user
    access_token = JwtService().create_access_token(data={"sub": str(user.id)})

    return access_token
