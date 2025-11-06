import uuid

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_structure():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic structure checks
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = f"test.user.{uuid.uuid4().hex}@example.com"

    # Ensure email is not present initially
    assert email not in activities[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_dup.status_code == 400

    # Unregister
    resp_un = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_returns_400():
    activity = "Chess Club"
    email = f"no.such.user.{uuid.uuid4().hex}@example.com"
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 400
