from django.urls import path

from .import views

urlpatterns = [
    path("", views.OrderListAPIView.as_view()),
    path("<uuid:order_id>/", views.OrderDetailApIView.as_view()),
]
