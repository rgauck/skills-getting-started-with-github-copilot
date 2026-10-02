from src.app import activities


def test_signup_new_student_returns_success_message(client):
    # Arrange
    activity_name = "Art Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_new_student_adds_participant(client):
    # Arrange
    activity_name = "Art Club"
    email = "student@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_duplicate_email_does_not_add_second_entry(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert activities[activity_name]["participants"].count(email) == 1


def test_signup_same_email_in_different_activity_succeeds(client):
    # Arrange
    email = activities["Chess Club"]["participants"][0]
    other_activity = "Art Club"

    # Act
    response = client.post(f"/activities/{other_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[other_activity]["participants"]


def test_signup_missing_email_returns_422(client):
    # Arrange
    activity_name = "Art Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
