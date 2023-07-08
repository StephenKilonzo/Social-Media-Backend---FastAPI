from .. app import schemas
import pytest
from jose import jwt
from app.config import settings



# @pytest.fixture
# def test_user(client):
#     user_data = {"username":"jackom@yahoo.com", "password": "jackom"}
#     res = client.post("/users/", json = user_data)
#     assert res.status_code == 201

#     new_user = res.json()
#     new_user["password"] = user_data["password"]
#     return new_user


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Welcome"
    assert res.status_code == 200 

def test_create_user(client):
    res = client.post("/users/", json={"email":"jackom@yahoo.com", "password": "jackom"})
    # use pydantic models
    new_user = schemas.UserOut(**res.json())
    assert new_user.json().get('email') == "jackom@yahoo.com"
    assert new_user.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user["email"], "password": test_user["password"]})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"

    assert res.status_code == 200
