import pytest
from rest_framework.test import APIRequestFactory

from apps.users.serializers import RegisterSerializer,  UpdateProfileSerializer, ChangePasswordSerializer
from factories import UserFactory


# =============== Start Test RegisterSerializer rejects duplicate email section ===============
@pytest.mark.django_db
def test_register_serializer_rejects_existing_email(user):
    serializer = RegisterSerializer(
        data={
            "username": "anotheruser",
            "email": user.email,
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        }
    )

    assert serializer.is_valid() is False
    assert "email" in serializer.errors
# =============== End Test RegisterSerializer rejects duplicate email seciton ===============


# =============== Start Test RegisterSerializer rejects mismatched passwords section ===============
@pytest.mark.django_db
def test_register_serializer_rejects_mismatched_passwords():
    serializer = RegisterSerializer(
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "DifferentPassword123!",
        }
    )

    assert serializer.is_valid() is False
    assert "confirm_password" in serializer.errors
# =============== End Test RegisterSerializer rejects mismatched passwords seciton ===============


# =============== Start Test ChangePasswordSerializer rejects incorrect old password section ===============
@pytest.mark.django_db
def test_change_password_serializer_rejects_wrong_old_password(user):
    request = APIRequestFactory().put("/")
    request.user = user
    serializer = ChangePasswordSerializer(
        data={
            "old_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
            "confirm_password": "NewPassword123!",
        },
        context={"request": request},
    )

    assert serializer.is_valid() is False
    assert "old_password" in serializer.errors
# =============== End Test ChangePasswordSerializer rejects incorrect old password seciton ===============


# =============== Start Test UpdateProfileSerializer email preventing use others email section ===============
@pytest.mark.django_db
def test_update_profile_serializer_rejects_another_users_email(user):
    another_user = UserFactory()

    serializer = UpdateProfileSerializer(
        instance=user,
        data={
            "username": user.username,
            "email": another_user.email,
        },
        partial=True,
    )

    assert serializer.is_valid() is False
    assert "email" in serializer.errors
# =============== End Test UpdateProfileSerializer email preventing use others email seciton ===============