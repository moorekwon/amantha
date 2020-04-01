from django.urls import path

from members.views import AuthTokenAPIView, CreateUserAPIView, LogoutUserAPIView, KaKaoLoginAPIView, KaKaoTemplate, \
    CreateUserProfileAPIView

urlpatterns = [
    path('auth/token/', AuthTokenAPIView.as_view()),
    path('auth/create/', CreateUserAPIView.as_view()),
    path('auth/logout/', LogoutUserAPIView.as_view()),
    path('auth/kakao/', KaKaoLoginAPIView.as_view()),
    path('auth/profile/', CreateUserProfileAPIView.as_view()),
    # path('auth/image/', ImageListAPIView.as_view()),
    # 테스트용 template (카카오톡 로그인 페이지)
    path('html/kakao/', KaKaoTemplate),
]
