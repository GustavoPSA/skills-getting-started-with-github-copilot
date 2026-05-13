import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original_activities


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_activity in activities
    assert "description" in activities[expected_activity]
    assert "participants" in activities[expected_activity]
    assert isinstance(activities[expected_activity]["participants"], list)


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    follow_up = client.get("/activities")
    participants = follow_up.json()[activity_name]["participants"]
    assert email in participants


def test_signup_for_activity_returns_400_when_already_registered():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
