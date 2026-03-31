import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine_test = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)
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


def test_create_item():
    r = client.post(
        "/api/items",
        json={"title": "Test item", "description": "Hello"}
    )
    assert r.status_code == 201
    assert r.json()["title"] == "Test item"


def test_list_items():
    r = client.get("/api/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_delete_item():
    r = client.post(
        "/api/items",
        json={"title": "To delete"}
    )
    item_id = r.json()["id"]
    r2 = client.delete(f"/api/items/{item_id}")
    assert r2.status_code == 200
    r3 = client.get(f"/api/items/{item_id}")
    assert r3.status_code == 404