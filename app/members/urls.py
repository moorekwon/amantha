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
    path('auth/kakao/', KaKaoLoginAPIView.as_view()),

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
    # GET, POST 유저가 pick한 이성 추가 및 조회, 유저를 pick한 이성 조회
    path('user/pick/', UserPickAPIView.as_view()),
    # GET, POST 유저가 가입심사한 이성과 보낸 별점 및 유저에게 가입심사한 이성과 받은 별점 조회, 이성 가입심사 별점 보내기
    path('user/star/', UserStarAPIView.as_view()),
    # GET, POST, PATCH 유저의 이상형 정보 설정 조회, 맞춤 이성 소개, 등록된 이상형 정보 수정
    path('user/ideal/', UserIdealTypeAPIView.as_view()),

    # GET 테마별 맞춤 이성(남자) 소개
    path('user/thema/', UserManThemaAPIView.as_view()),

    # GET 유저의 태그 전체 조회
    # PATCH 추후 추가... (현재는 아래 4개 url 주소로 태그타입별 각각 PATCH 설정)
    path('user/tag/', UserTagAPIView.as_view()),
    # PATCH 유저의 데이트 스타일 태그 수정
    path('user/tag/date/', UserTagDateStyleAPIView.as_view()),
    # PATCH 유저의 라이프 스타일 태그 수정
    path('user/tag/life/', UserTagLifeStyleAPIView.as_view()),
    # PATCH 유저의 나만의 매력 태그 수정
    path('user/tag/charm/', UserTagCharmAPIView.as_view()),
    # PATCH 유저의 연애 스타일 태그 수정
    path('user/tag/relationship/', UserTagRelationshipAPIView.as_view()),

    # 테스트용 template (카카오톡 로그인 페이지)
    path('html/kakao/', KaKaoTemplate),
]
