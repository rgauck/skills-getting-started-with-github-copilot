from src.app import activities


def test_unregister_existing_participant_returns_success_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}


def test_unregister_existing_participant_removes_them(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_student_not_signed_up_returns_404(client):
    # Arrange
    activity_name = "Art Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_signup_after_unregister_succeeds(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]
    activities[activity_name]["participants"].remove(email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
