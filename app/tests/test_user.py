from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_create_user():
    response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_get_existed_user():
    # Create a user first
    create_resp = client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})
    user_id = create_resp.json()["id"]

    # Get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"


def test_get_not_existed_user():
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_update_user():
    # Create a user first
    create_resp = client.post("/users/", json={"name": "Charlie", "email": "charlie@example.com"})
    user_id = create_resp.json()["id"]

    # Update the user
    response = client.put(f"/users/{user_id}", json={"name": "Charlie Updated", "email": "charlie@new.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Charlie Updated"
    assert data["email"] == "charlie@new.com"


def test_delete_user():
    # Create a user first
    create_resp = client.post("/users/", json={"name": "Dave", "email": "dave@example.com"})
    user_id = create_resp.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404