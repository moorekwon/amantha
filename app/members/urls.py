from django.urls import path

from members.views import AuthTokenAPIView, CreateUserAPIView, LogoutUserAPIView

urlpatterns = [
    path('auth/login/', AuthTokenAPIView.as_view(), name='login'),
    path('auth/signup/', CreateUserAPIView.as_view(), name='signup'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='logout'),
]
