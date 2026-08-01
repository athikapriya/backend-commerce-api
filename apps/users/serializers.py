from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


# =============== Start RegisterSerializer section ===============
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type" : "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input_type" : "password"})

    class Meta:
        model = User
        fields = (
            "username", 
            "email", 
            "password", 
            "confirm_password",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
# =============== End RegisterSerializer seciton ===============


# =============== Start LogoutSerializer section ===============
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        try:
            RefreshToken(self.validated_data["refresh"]).blacklist()

        except TokenError:
            raise serializers.ValidationError(
                {
                    "refresh": "Invalid or expired refresh token."
                }
            )
# =============== End LogoutSerializer seciton ===============


# =============== Start UserProfileSerializer section ===============
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "is_staff",
            "date_joined",
        )
# =============== End UserProfileSerializer seciton ===============


# =============== Start UpdateProfileSerializer section ===============
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate_email(self, value):
        user = self.instance

        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )
        return value
# =============== End UpdateProfileSerializer seciton ===============


# =============== Start ChangePasswordSerializer section ===============
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is incorrect."
            )
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(
            self.validated_data["new_password"]
        )
        user.save()
# =============== End ChangePasswordSerializer seciton ===============