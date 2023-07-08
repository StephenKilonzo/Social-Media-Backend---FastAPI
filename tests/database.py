from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
from alembic import command



# add test db
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
    

# app.dependency_overrides[get_db] = override_get_db



# client = TestClient(app)

@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine) #drop any exixting table before creating
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    # run code before we run test
    # Base.metadata.drop_all(bind=engine) #drop any exixting table before creating
    # Base.metadata.create_all(bind=engine)
    # command.upgrade("head")

    # yield TestClient(app)
    # run code after we run test
    # Base.metadata.drop_all(bind=engine)
    # command.downgrade("base")

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)