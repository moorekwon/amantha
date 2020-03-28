from django.urls import path

from members.views import AuthTokenAPIView

urlpatterns = [
    path('auth-token/', AuthTokenAPIView.as_view(), name='login'),

]
