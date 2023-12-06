from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.BaseModel import EntityMeta
from app.config.Database import get_db_connection
from app.main import app
from app.models.UserModel import UserModel
from app.utils.security import SecurityUtils
from app.services.JwtService import JwtService
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


EntityMeta.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_connection] = override_get_db


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
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
