from rest_framework import generics, status
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import RegisterSerializer, LogoutSerializer, UserProfileSerializer, UpdateProfileSerializer, ChangePasswordSerializer


# =============== Start RegisterAPIView section ===============
@extend_schema(
    summary="Register User",
    description="Create a new customer account.",
    tags=["Authentication"],
)
class RegisterAPIView(generics.CreateAPIView):
    throttle_scope = "register"
    serializer_class = RegisterSerializer
# =============== End RegisterAPIView seciton ===============


# =============== Start LoginAPIView section ===============
@extend_schema(
    summary="Login User",
    description="Authenticate a user and return JWT access and refresh tokens.",
    tags=["Authentication"],
)
class LoginAPIView(TokenObtainPairView):
    throttle_scope = "login"
# =============== End LoginAPIView seciton ===============


# =============== Start LogoutAPIView section ===============
@extend_schema(
    summary="Logout User",
    description="Blacklist the refresh token and log out the authenticated user.",
    tags=["Authentication"],
)
class LogoutAPIView(generics.GenericAPIView):
    throttle_scope = "logout"
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail" : "Logged out successfully."},
            status=status.HTTP_205_RESET_CONTENT,
        )
# =============== End LogoutAPIView seciton ===============


# =============== Start UserProfileAPIView section ===============
@extend_schema_view(
    get=extend_schema(
        summary="Current User",
        description="Retrieve the authenticated user's profile.",
        tags=["Authentication"],
    ),
    put=extend_schema(
        summary="Update Profile",
        description="Replace username and email.",
        tags=["Authentication"],
    ),
    patch=extend_schema(
        summary="Partially Update Profile",
        description="Update username or email.",
        tags=["Authentication"],
    ),
)
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    throttle_scope = "profile"
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateProfileSerializer
        return UserProfileSerializer
# =============== End UserProfileAPIView seciton ===============


# =============== Start ChangePasswordAPIView section ===============
@extend_schema(
    summary="Change Password",
    description="Change the authenticated user's password.",
    tags=["Authentication"],
)
class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = "change_password"

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )
# =============== End ChangePasswordAPIView seciton ===============