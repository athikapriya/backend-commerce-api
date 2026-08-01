from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import RegisterSerializer


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