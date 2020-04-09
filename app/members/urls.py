from django.urls import path

from members.views import *

urlpatterns = [
    # POST 유저 회원가입
    path('auth/create/', CreateUserAPIView.as_view()),
    # POST 유저 로그인 / GET 전체 유저 조회
    path('auth/token/', AuthTokenAPIView.as_view()),
    # POST 유저 로그아웃
    path('auth/logout/', LogoutUserAPIView.as_view()),
    # POST 유저 카카오톡 로그인
    # path('auth/kakao/', KaKaoLoginAPIView.as_view()),

    # 유저의 모든 상세프로필 정보 조회
    path('user/profile/', UserProfileAPIView.as_view()),
    # GET,POST UserImage 정보
    path('user/image/', UserImageAPIView.as_view()),
    # DELETE 유저의 image 객체 정보
    path('user/image/<int:pk>/', UserImageAPIView.as_view()),
    # GET, POST, PATCH UserInfo 정보
    path('user/info/', UserInfoAPIView.as_view()),
    # GET, POST SelectStory 정보
    path('user/story/', UserStoryAPIView.as_view()),
    # DELETE 유저의 story 객체 정보
    path('user/story/<int:pk>/', UserStoryAPIView.as_view()),
    # GET, POST 유저의 리본내역 조회 및 리본지급 추가
    path('user/ribbon/', UserRibbonAPIView.as_view()),
    # GET, PATCH 유저의 태그 조회 및 추가(수정)
    path('user/tag/', UserTagAPIView.as_view()),

    # 테스트용 template (카카오톡 로그인 페이지)
    path('html/kakao/', KaKaoTemplate),
]
