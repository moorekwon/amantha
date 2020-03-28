from django.urls import path

from members.views import AuthTokenAPIView, CreateUserAPIView

urlpatterns = [
    path('auth-token/', AuthTokenAPIView.as_view(), name='login'),
    path('create/', CreateUserAPIView.as_view(), name='signup'),
]
