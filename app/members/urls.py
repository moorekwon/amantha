from django.urls import path

from members.views import AuthTokenAPIView, CreateUserAPIView, LogoutUserAPIView, KaKaoLoginAPIView, KaKaoTemplate

urlpatterns = [
    path('auth/login/', AuthTokenAPIView.as_view(), name='login'),
    path('auth/signup/', CreateUserAPIView.as_view(), name='signup'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('auth/kakao/', KaKaoLoginAPIView.as_view(), name='login-kakao'),
    # path('auth/signup/profile/', CreateUserProfileAPIView.as_view(), name='signup-profile'),
    # 테스트용 template (카카오톡 로그인 페이지)
    path('html/kakao/', KaKaoTemplate, name='kakao-html'),
]
