from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register",),
    path("login/", LoginAPIView.as_view(), name="login",),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh",),

    path("profile/", UserProfileAPIView.as_view(), name="profile"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("forget-password/", ForgetPasswordAPIView.as_view(), name="forget_passwrord"),
    path("reset-password/<uid>/<token>/", ResetPasswordAPIView.as_view(), name="reset_password",),
]
