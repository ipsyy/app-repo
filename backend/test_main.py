import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# Use SQLite in-memory for tests — no MySQL needed
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine_test = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_list_item():
    r = client.post("/api/items", json={"title": "Test item", "description": "Hello"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test item"

    r2 = client.get("/api/items")
    assert r2.status_code == 200
    assert any(i["title"] == "Test item" for i in r2.json())


def test_delete_item():
    r = client.post("/api/items", json={"title": "To delete"})
    item_id = r.json()["id"]

    r2 = client.delete(f"/api/items/{item_id}")
    assert r2.status_code == 200

    r3 = client.get(f"/api/items/{item_id}")
    assert r3.status_code == 404
```

---

## `app-repo/backend/.env.example`
```
ENVIRONMENT=dev
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=appdb_dev
DB_USER=appuser_dev
DB_PASSWORD=changeme
BACKEND_PORT=8000