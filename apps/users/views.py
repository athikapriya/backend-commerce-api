from rest_framework import generics, status
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import *
from .tasks import send_welcome_email


# =============== Start RegisterAPIView section ===============
@extend_schema(
    summary="Register User",
    description="Create a new customer account.",
    tags=["Authentication"],
)
class RegisterAPIView(generics.CreateAPIView):
    throttle_scope = "register"
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        send_welcome_email.delay(
            user.email,
            user.username,
        )
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


# =============== Start ForgetPasswordAPIView section ===============
@extend_schema(
    summary="Forgot Password",
    description="Send a password reset email.",
    tags=["Authentication"],
)
class ForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    throttle_scope = "forget_password"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail" : "Password reset email sent."},
            status=status.HTTP_200_OK,
        )
# =============== End ForgetPasswordAPIView seciton ===============


# =============== Start ResetPasswordAPIView section ===============
@extend_schema(
    summary="Reset Password",
    description="Reset password using the uid and token sent by email.",
    tags=["Authentication"],
)
class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    throttle_scope = "forget_password"

    def post(self, request, uid, token):
        serializer = self.get_serializer(
            data=request.data,
            context={
                "uid": uid,
                "token": token,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
# =============== End ResetPasswordAPIView seciton ===============