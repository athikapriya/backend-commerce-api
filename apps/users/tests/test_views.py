import pytest
from rest_framework import status

from factories import UserFactory


# =============== Start Test registration section ===============
@pytest.mark.django_db
def test_user_can_register(api_client):
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
    }

    response = api_client.post("/api/users/register/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"
    assert response.data["email"] == "newuser@example.com"
# =============== End Test registration seciton ===============


# =============== Start Test duplicate email section ===============
@pytest.mark.django_db
def test_user_cannot_register_with_existing_email(api_client, user):
    payload = {
        "username": "anotheruser",
        "email": user.email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
    }

    response = api_client.post("/api/users/register/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
# =============== End Test duplicate email seciton ===============


# =============== Start Test password confirmation section ===============
@pytest.mark.django_db
def test_user_cannot_register_with_mismatched_passwords(api_client):
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "StrongPassword123!",
        "confirm_password": "DifferentPassword123!",
    }

    response = api_client.post("/api/users/register/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "confirm_password" in response.data
# =============== End Test password confirmation seciton ===============


# =============== Start Test unauthenticated profile access section ===============
@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_profile(api_client):
    response = api_client.get("/api/users/profile/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
# =============== End Test unauthenticated profile access seciton ===============


# =============== Start Test authenticated profile access section ===============
@pytest.mark.django_db
def test_authenticated_user_can_access_profile(api_client, user):
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/users/profile/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email
# =============== End Test authenticated profile access seciton ===============


# =============== Start Test profile update section ===============
@pytest.mark.django_db
def test_user_can_update_profile(api_client, user):
    api_client.force_authenticate(user=user)

    payload = {
        "username": "updatedusername",
        "email": "updated@example.com",
    }

    response = api_client.patch("/api/users/profile/", payload, format="json")
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()

    assert user.username == "updatedusername"
    assert user.email == "updated@example.com"
# =============== End Test profile update seciton ===============


# =============== Start Test logout section ===============
@pytest.mark.django_db
def test_user_can_logout(api_client, user):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/api/users/logout/",
        {"refresh": str(refresh)},
        format="json",
    )

    assert response.status_code == status.HTTP_205_RESET_CONTENT
# =============== End Test logout seciton ===============


# =============== Start Test change password section ===============
@pytest.mark.django_db
def test_user_can_change_password(api_client, user):
    api_client.force_authenticate(user=user)

    payload = {
        "old_password": "TestPassword123!",
        "new_password": "NewPassword123!",
        "confirm_password": "NewPassword123!",
    }

    response = api_client.put("/api/users/change-password/", payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password("NewPassword123!")
# =============== End Test change password seciton ===============


# =============== Start Test incorrect old password section ===============
@pytest.mark.django_db
def test_user_cannot_change_password_with_wrong_old_password(api_client, user):
    api_client.force_authenticate(user=user)

    payload = {
        "old_password": "WrongPassword123!",
        "new_password": "NewPassword123!",
        "confirm_password": "NewPassword123!",
    }

    response = api_client.put("/api/users/change-password/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "old_password" in response.data
# =============== End Test incorrect old password seciton ===============


# =============== Start Test password mismatch section ===============
@pytest.mark.django_db
def test_user_cannot_change_password_when_passwords_do_not_match(api_client, user):
    api_client.force_authenticate(user=user)

    payload = {
        "old_password": "TestPassword123!",
        "new_password": "NewPassword123!",
        "confirm_password": "DifferentPassword123!",
    }

    response = api_client.put("/api/users/change-password/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "confirm_password" in response.data
# =============== End Test password mismatch seciton ===============


# =============== Start Test forgot password section ===============
@pytest.mark.django_db
def test_user_can_request_password_reset(api_client, user, mailoutbox):
    response = api_client.post(
        "/api/users/forget-password/",
        {"email": user.email},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(mailoutbox) == 1
    assert user.email in mailoutbox[0].to
# =============== End Test forgot password seciton ===============


# =============== Start Test nonexistent email section ===============
@pytest.mark.django_db
def test_password_reset_fails_for_unknown_email(api_client):
    response = api_client.post(
        "/api/users/forget-password/",
        {"email": "doesnotexist@example.com"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
# =============== End Test nonexistent email seciton ===============