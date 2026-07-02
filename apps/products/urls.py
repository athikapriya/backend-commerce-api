from django.urls import path

from . import views


urlpatterns = [
    path("", views.ProductAPIView.as_view()),
    path("<slug:slug>/", views.ProductDetailsAPIView.as_view()),
]
