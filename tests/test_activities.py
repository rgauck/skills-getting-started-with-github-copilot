from src.app import activities

EXPECTED_KEYS = {"description", "schedule", "max_participants", "participants"}


def test_get_activities_returns_200(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_names = set(activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert set(response.json().keys()) == expected_names
    assert len(expected_names) == 9


def test_get_activities_each_activity_has_expected_fields(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    for name, details in response.json().items():
        assert set(details.keys()) == EXPECTED_KEYS, name
        assert isinstance(details["participants"], list), name


def test_get_activities_reflects_current_participants(client):
    # Arrange
    activities["Chess Club"]["participants"].append("new@mergington.edu")

    # Act
    response = client.get("/activities")

    # Assert
    assert "new@mergington.edu" in response.json()["Chess Club"]["participants"]
